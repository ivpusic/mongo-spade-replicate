from pydispatch import dispatcher
from pymongo import MongoClient

SIGNAL_ADD = 'ADD'
SIGNAL_REMOVE = 'REMOVE'
SIGNAL_UPDATE = 'UPDATE'
client = MongoClient()


def trigger_add(data, db_info):
    '''
    add data to db, and notify spade about that
    '''
    db = client[db_info['db']]
    collection = db[db_info['collection']]
    data['_id'] = collection.insert(data)
    dispatcher.send(signal=SIGNAL_ADD, sender=data)


def register_add(callback):
    dispatcher.connect(callback, signal=SIGNAL_ADD, sender=dispatcher.Any)


def register_update(callback):
    dispatcher.connect(callback, signal=SIGNAL_UPDATE, sender=dispatcher.Any)
