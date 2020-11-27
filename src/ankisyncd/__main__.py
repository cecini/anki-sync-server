import sys
import tracemalloc
# PYTHONMALLOCSTATS=1
# PYTHONTRACEMALLOC=25
tracemalloc.start(25)

#import gc
#gc.disable()
#import orjson
#import decimal



if __package__ is None and not hasattr(sys, "frozen"):
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import ankisyncd.sync_app

def default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError


if __name__ == "__main__":
   # orjson.dumps([])
   # orjson.dumps(decimal.Decimal("3.141592653"))
   # orjson.dumps(decimal.Decimal("3.141592653"), default=default)
    ankisyncd.sync_app.main()


#snapshot = tracemalloc.take_snapshot()
#top_stats = snapshot.statistics('lineno')

#print("[ Top 10 ]")
#for stat in top_stats[:10]:
#    print(stat)


#snapshot = tracemalloc.take_snapshot()
#top_stats = snapshot.statistics('traceback')

## pick the biggest memory block
#stat = top_stats[0]
#print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
#for line in stat.traceback.format():
#    print(line)


