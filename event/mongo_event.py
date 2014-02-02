from pydispatch import dispatcher
from pymongo import MongoClient
from event.action import ADD
from bson.objectid import ObjectId


SIGNAL_ADD = 'ADD'
SIGNAL_REMOVE = 'REMOVE'
SIGNAL_UPDATE = 'UPDATE'
client = MongoClient()


def trigger_add(data, db_info, replicated=False):
    '''
    add data to db, and notify spade about that
    '''
    db = client[db_info['db']]
    collection = db[db_info['collection']]

    if replicated:
        dt = collection.find_one({'id': ObjectId(data['_id'])})
        print dt
        if dt:
            print 'data already replicated...'
            return

    for res in collection.find():
        print res

    data['_id'] = collection.insert(data)
    to_send = {}
    to_send['db'] = {
        'db': db_info['db'],
        'collection': db_info['collection'],
        'action': ADD
    }
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_ADD, sender=to_send)


def register_add(callback):
    dispatcher.connect(callback, signal=SIGNAL_ADD, sender=dispatcher.Any)


def register_update(callback):
    dispatcher.connect(callback, signal=SIGNAL_UPDATE, sender=dispatcher.Any)
