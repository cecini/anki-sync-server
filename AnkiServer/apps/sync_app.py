
# AnkiServer - A personal Anki sync server
# Copyright (C) 2013 David Snopek
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from webob.dec import wsgify
from webob.exc import *
from webob import Response

import sqlite3
import hashlib

import AnkiServer

import anki
from anki.sync import Syncer, MediaSyncer

try:
    import simplejson as json
except ImportError:
    import json

import os

class SyncCollectionHandler(Syncer):
    operations = ['meta', 'applyChanges', 'start', 'chunk', 'applyChunk', 'sanityCheck2', 'finish']

    def __init__(self, col):
        # So that 'server' (the 3rd argument) can't get set
        Syncer.__init__(self, col)

class SyncMediaHandler(MediaSyncer):
    operations = ['remove', 'files', 'addFiles', 'mediaSanity', 'mediaList']

    def __init__(self, col):
        MediaSyncer.__init__(self, col)

    # TODO: This function is mostly just a placeholder that doesn't crash... Make it actually work!
    def files(self, minUsn=0, need=[], fnames=[]):
        """Gets files from the media database and returns them as ZIP file data."""

        import zipfile, StringIO

        # TODO: Do something with minUsn, need and fnames!
        # TODO: I think we're going to have to reimplement this function with changes for
        #       the minUsn, need and fnames...
        zipdata, fnames = self.col.media.zipAdded()

        # add a _usn element to the zipdata
        fd = StringIO.StringIO(zipdata)
        zfd = zipfile.ZipFile(fd, "a", compression=zipfile.ZIP_DEFLATED)
        # TODO: what does this value represent? How can we get it?
        zfd.writestr("_usn", str(minUsn + len(fnames)))
        zfd.close()

        return fd.getvalue()

    def mediaList(self):
        """Returns a list of all the fnames in this collections media database."""
        fnames = []
        for fname in self.col.media.db.execute("select fname from media"):
            fnames.append(fname)
        return fnames

class SyncUserSession(object):
    def __init__(self, name, path, collection_manager):
        import time
        self.name = name
        self.path = path
        self.collection_manager = collection_manager
        self.version = 0
        self.created = time.time()

        # make sure the user path exists
        if not os.path.exists(path):
            os.mkdir(path)

        self.collection_handler = None
        self.media_handler = None

    def get_collection_path(self):
        return os.path.realpath(os.path.join(self.path, 'collection.anki2'))

    def get_thread(self):
        return self.collection_manager.get_collection(self.get_collection_path())

    def get_handler_for_operation(self, operation, col):
        if operation in SyncCollectionHandler.operations:
            cache_name, handler_class = 'collection_handler', SyncCollectionHandler
        else:
            cache_name, handler_class = 'media_handler', SyncMediaHandler

        if getattr(self, cache_name) is None:
            setattr(self, cache_name, handler_class(col))
        return getattr(self, cache_name)

class SyncApp(object):
    valid_urls = SyncCollectionHandler.operations + SyncMediaHandler.operations + ['hostKey', 'upload', 'download', 'getDecks']

    def __init__(self, **kw):
        from AnkiServer.threading import getCollectionManager

        self.data_root = os.path.abspath(kw.get('data_root', '.'))
        self.base_url  = kw.get('base_url', '/')
        self.auth_db_path = os.path.abspath(kw.get('auth_db_path', '.'))
        self.sessions = {}

        try:
            self.collection_manager = kw['collection_manager']
        except KeyError:
            self.collection_manager = getCollectionManager()

        # make sure the base_url has a trailing slash
        if len(self.base_url) == 0:
            self.base_url = '/'
        elif self.base_url[-1] != '/':
            self.base_url = base_url + '/'

    def authenticate(self, username, password):
        """
        Returns True if this username is allowed to connect with this password. False otherwise.

        Override this to change how users are authenticated.
        """

        return False

    def username2dirname(self, username):
        """
        Returns the directory name for the given user. By default, this is just the username.

        Override this to adjust the mapping between users and their directory.
        """

        return username

    def generateHostKey(self, username):
        """Generates a new host key to be used by the given username to identify their session.
        This values is random."""

        import hashlib, time, random, string
        chars = string.ascii_letters + string.digits
        val = ':'.join([username, str(int(time.time())), ''.join(random.choice(chars) for x in range(8))])
        return hashlib.md5(val).hexdigest()

    def create_session(self, hkey, username, user_path):
        """Creates, stores and returns a new session for the given hkey and username."""

        session = self.sessions[hkey] = SyncUserSession(username, user_path, self.collection_manager)
        return session

    def load_session(self, hkey):
        return self.sessions.get(hkey)

    def save_session(self, hkey, session):
        pass

    def delete_session(self, hkey):
        del self.sessions[hkey]

    def _decode_data(self, data, compression=0):
        import gzip, StringIO

        if compression:
            buf = gzip.GzipFile(mode="rb", fileobj=StringIO.StringIO(data))
            data = buf.read()
            buf.close()

        # really lame check for JSON
        if data[0] == '{' and data[-1] == '}':
            data = json.loads(data)
        else:
            data = {'data': data}

        return data

    def operation_upload(self, col, data, session):
        col.close()
        # TODO: we should verify the database integrity before perminantly overwriting
        # (ie. use a temporary file) and declaring this a success!
        #
        # d = DB(path)
        # assert d.scalar("pragma integrity_check") == "ok"
        # d.close()
        #
        try:
            with open(session.get_collection_path(), 'wb') as fd:
                fd.write(data)
        finally:
            col.reopen()
        
        return True

    def operation_download(self, col, session):
        col.close()
        data = open(session.get_collection_path(), 'rb').read()
        col.reopen()
        return data

    @wsgify
    def __call__(self, req):
        print req.path
        if req.path.startswith(self.base_url):
            url = req.path[len(self.base_url):]
            if url not in self.valid_urls:
                raise HTTPNotFound()

            if url == 'getDecks':
                # This is an Anki 1.x client! Tell them to upgrade.
                import zlib
                return Response(
                        status='200 OK',
                        content_type='application/json',
                        content_encoding='deflate',
                        body=zlib.compress(json.dumps({'status': 'oldVersion'})))

            try:
                compression = req.POST['c']
            except KeyError:
                compression = 0

            try:
                data = req.POST['data'].file.read()
                data = self._decode_data(data, compression)
            except KeyError:
                data = {}
            except ValueError:
                # Bad JSON
                raise HTTPBadRequest()
            print 'data:', data

            if url == 'hostKey':
                try:
                    u = data['u']
                    p = data['p']
                except KeyError:
                    raise HTTPForbidden('Must pass username and password')
                if self.authenticate(u, p):
                    dirname = self.username2dirname(u)
                    if dirname is None:
                        raise HTTPForbidden()

                    hkey = self.generateHostKey(u)
                    user_path = os.path.join(self.data_root, dirname)
                    session = self.create_session(hkey, u, user_path)

                    result = {'key': hkey}
                    return Response(
                        status='200 OK',
                        content_type='application/json',
                        body=json.dumps(result))
                else:
                    # TODO: do I have to pass 'null' for the client to receive None?
                    raise HTTPForbidden('null')

            # Get and verify the session
            try:
                hkey = req.POST['k']
            except KeyError:
                raise HTTPForbidden()
            session = self.load_session(hkey)
            if session is None:
                raise HTTPForbidden()

            if url in SyncCollectionHandler.operations + SyncMediaHandler.operations:
                # 'meta' passes the SYNC_VER but it isn't used in the handler
                if url == 'meta' and data.has_key('v'):
                    session.version = data['v']
                    del data['v']

                # Create a closure to run this operation inside of the thread allocated to this collection
                def runFunc(col):
                    handler = session.get_handler_for_operation(url, col)
                    func = getattr(handler, url)
                    result = func(**data)
                    handler.col.save()
                    return result
                runFunc.func_name = url

                # Send to the thread to execute
                thread = session.get_thread()
                result = thread.execute(runFunc)

                # If it's a complex data type, we convert it to JSON
                if type(result) not in (str, unicode):
                    result = json.dumps(result)

                # TODO: Apparently 'finish' isn't when we're done because 'mediaList' comes after it...
                #       When can we possibly delete the session?

                #if url == 'finish':
                #    self.delete_session(hkey)

                return Response(
                    status='200 OK',
                    content_type='application/json',
                    body=result)

            elif url == 'upload':
                thread = session.get_thread()
                result = thread.execute(self.operation_upload, [data['data'], session])
                return Response(
                    status='200 OK',
                    content_type='text/plain',
                    body='OK' if result else 'Error')

            elif url == 'download':
                thread = session.get_thread()
                result = thread.execute(self.operation_download, [session])
                return Response(
                    status='200 OK',
                    content_type='text/plain',
                    body=result)

            # This was one of our operations but it didn't get handled... Oops!
            raise HTTPInternalServerError()

        return Response(status='200 OK', content_type='text/plain', body='Anki Sync Server')

class DatabaseAuthSyncApp(SyncApp):
    def authenticate(self, username, password):
        """Returns True if this username is allowed to connect with this password. False otherwise."""

        conn = sqlite3.connect(self.auth_db_path)
        cursor = conn.cursor()
        param = (username,)

        cursor.execute("SELECT hash FROM auth WHERE user=?", param)

        db_ret = cursor.fetchone()

        if db_ret != None:
            db_hash = str(db_ret[0])
            salt = db_hash[-16:]
            hashobj = hashlib.sha256()

            hashobj.update(username+password+salt)

        return (db_ret != None and hashobj.hexdigest()+salt == db_hash)

# Our entry point
def make_app(global_conf, **local_conf):
    return DatabaseAuthSyncApp(**local_conf)

def main():
    from wsgiref.simple_server import make_server
    from AnkiServer.threading import shutdown

    ankiserver = SyncApp()
    httpd = make_server('', 8001, ankiserver)
    try:
        print "Starting..."
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Exiting ..."
    finally:
        shutdown()

if __name__ == '__main__': main()
