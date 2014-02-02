from pydispatch import dispatcher
from pymongo import MongoClient
from event.action import ADD, UPDATE, DELETE
from event.action import SIGNAL_ADD, SIGNAL_REMOVE, SIGNAL_UPDATE
from bson.objectid import ObjectId

client = MongoClient()


def no_id_error(operation):
    print 'You must provide _id for ', operation
    return


def no_data_error():
    print 'There is no required data on mongo server!'
    return


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

    if '_id' in data:
        dt = collection.find_one({'_id': ObjectId(data['_id'])})
        if dt:
            return

    data['_id'] = collection.insert(data)
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_ADD, sender=to_send)


def trigger_update(data, db_info, replicated=False):

    if '_id' not in data:
        return no_id_error(UPDATE)

    dt = prepare(db_info, UPDATE)
    collection = dt[0]
    to_send = dt[1]

    existing_data = collection.find_one({'_id': ObjectId(data['_id'])})
    if not existing_data:
        return no_data_error()
    else:
        if existing_data == data:
            return

    collection.save(data)
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_UPDATE, sender=to_send)


def trigger_delete(data, db_info, replicated=False):

    if '_id' not in data:
        return no_id_error(DELETE)

    dt = prepare(db_info, DELETE)
    collection = dt[0]
    to_send = dt[1]

    existing_data = collection.find_one({'_id': ObjectId(data['_id'])})
    if not existing_data:
        return no_data_error()

    to_send['data'] = data
    collection.remove(data)
    dispatcher.send(signal=SIGNAL_REMOVE, sender=to_send)


def register_add(callback):
    dispatcher.connect(callback, signal=SIGNAL_ADD, sender=dispatcher.Any)


def register_update(callback):
    dispatcher.connect(callback, signal=SIGNAL_UPDATE, sender=dispatcher.Any)


def register_delete(callback):
    dispatcher.connect(callback, signal=SIGNAL_REMOVE, sender=dispatcher.Any)
