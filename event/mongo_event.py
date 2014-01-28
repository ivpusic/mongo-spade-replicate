from pydispatch import dispatcher
from pymongo import MongoClient

SIGNAL_ADD = 'ADD'
SIGNAL_REMOVE = 'REMOVE'
SIGNAL_UPDATE = 'UPDATE'
client = MongoClient()

def trigger_add(data):
    db = client[data['db']]
    collection = db[data['collection']]
    del data['db']
    del data['collection']
    data['_id'] = collection.insert(data)
    dispatcher.send(signal=SIGNAL_ADD, sender=data)

def register_add(callback):
    dispatcher.connect(callback, signal=SIGNAL_ADD, sender=dispatcher.Any)
