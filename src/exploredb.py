from anki import Collection
from anki.utils import intTime
import time
import argparse

parser = argparse.ArgumentParser()
#parser.add_argument("colpath", help="collection path")
parser.add_argument("--colpath", help="collection path")
parser.add_argument("--server", help="server mode true or false", type=bool)
args = parser.parse_args()

collection_path = "./collections/rourou/collection.anki2"
if args.colpath:
    collection_path = args.colpath

if args.server == None:
     args.server = True
# col = Collection(collection_path, server=True)
col = Collection(collection_path, server=args.server)

print(f'Collection Name: {col.name()}')
print(f'Cards in Collection: {col.noteCount()}')


print('Decks:')
for deck in col.decks.all():
    print(f"{deck['id']}. {deck['name']}")

deck_id = None
print('Cards in deck:')
i = 0
for card_id in col.decks.cids(deck_id):
    i+=1
    print(f'{i}. {card_id}')

# card_id = None
# print('Notes in card:')
# note_id = col.getCard(card_id).nid
# print(f"1. Front: {col.getNote(note_id).fields[0]}")
# print(f"2. Back: {col.getNote(note_id).fields[1]}")

print('graves in deck:')
# print(col.backend.col.storage)
# should use python api 
# thsi db is dbproxy 
#print(col.db.list("select oid from graves"))
#print(col.db.list("select usn from graves"))
#col.reopen()
#failback??
#why also ok?
#import pdb;pdb.set_trace()
#dbproxy all accepyt?why
   # execute used to return a pysqlite cursor, but now is synonymous
# 15     # with .all()
# 14     execute = all
#print(col.db.execute("select oid from graves"))

#col.db.list("select id from col")
#import pdb;pdb.set_trace()
#col.db.list("select id from cards")


#print(col.db.list("select * from graves"))
#print(col.db.execute("select * from graves"))
for i in col.db.execute("select * from graves"):
   # print(i)
  #  for j,k,l in i:
  #      if l == 0:
  #          print(str(j) + ":" + str(k) + ":" + "card")
  #      if l == 1:
  #          print(str(j) + ":" + str(k) + ":" + "note")
  #      if l == 2:
  #          print(str(j) + ":" + str(k) + ":" + "deck")
    if i[2] == 0:
        print(str(i[0]) + "------" + str(i[1]) + "------" + "card")
    if i[2] == 1:
        print(str(i[0]) + "------" + str(i[1]) + "------" + "note")
    if i[2] == 2:
        print(str(i[0]) + "------" + str(i[1]) + "------" + "deck")
   # print(i)

    
print("col ver:" + str(col.db.execute("select ver from col")))
print("col scm:" + str(col.db.execute("select scm from col")))

col.close()



