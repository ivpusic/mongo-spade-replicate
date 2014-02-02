from pydispatch import dispatcher
from pymongo import MongoClient
from event.action import ADD, UPDATE
from bson.objectid import ObjectId


SIGNAL_ADD = 'ADD'
SIGNAL_REMOVE = 'REMOVE'
SIGNAL_UPDATE = 'UPDATE'
client = MongoClient()


def prepare(db_info, operation):
    db = client[db_info['db']]
    collection = db[db_info['collection']]
    to_send = {}
    to_send['db'] = {
        'db': db_info['db'],
        'collection': db_info['collection'],
        'action': operation
    }

    return collection, to_send


def trigger_add(data, db_info, replicated=False):
    '''
    add data to db, and notify spade about that
    '''
    dt = prepare(db_info, ADD)
    collection = dt[0]
    to_send = dt[1]

    if replicated:
        dt = collection.find_one({'_id': ObjectId(data['_id'])})
        if dt:
            print 'data already replicated...'
            return

    data['_id'] = collection.insert(data)
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_ADD, sender=to_send)


def trigger_update(data, db_info, replicated=False):

    dt = prepare(db_info, UPDATE)
    collection = dt[0]
    to_send = dt[1]

    existing_data = collection.find_one({'_id': ObjectId(data['_id'])})
    if not existing_data:
        print 'data does not exits...'
        return
    else:
        print 'data exist....'
        print existing_data
        print data
        if existing_data == data:
            print 'data already updated...'
            return
    collection.save(data)
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_UPDATE, sender=to_send)


def register_add(callback):
    dispatcher.connect(callback, signal=SIGNAL_ADD, sender=dispatcher.Any)


def register_update(callback):
    dispatcher.connect(callback, signal=SIGNAL_UPDATE, sender=dispatcher.Any)
