from pydispatch import dispatcher
from pymongo import MongoClient
from event.action import ADD, UPDATE, DELETE
from event.action import SIGNAL_ADD, SIGNAL_REMOVE, SIGNAL_UPDATE
from bson.objectid import ObjectId
from log.mongo_log import make_log

client = MongoClient()


def no_id_error(operation):
    print 'You must provide _id for ', operation
    return


def no_data_error():
    print 'Skipping action...!'
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

        dt = collection.find_one({'_id': data['_id']})
        if dt:
            return
        data['_id'] = ObjectId(data['_id'])

    data['_id'] = str(collection.insert(data))
    to_send['log'] = make_log(db_info['db'], db_info['collection'], str(data['_id']), ADD)
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_ADD, sender=to_send)


def trigger_update(data, db_info, replicated=False):

    if '_id' not in data:
        return no_id_error(UPDATE)
    else:
        data['_id'] = str(data['_id'])

    dt = prepare(db_info, UPDATE)
    collection = dt[0]
    to_send = dt[1]

    existing_data = collection.find_one({'_id': ObjectId(data['_id'])})
    if not existing_data:
        return no_data_error()
    else:
        data['_id'] = ObjectId(data['_id'])
        print existing_data
        print data
        if existing_data == data:
            return

    collection.save(data)
    data['_id'] = str(data['_id'])
    to_send['log'] = make_log(db_info['db'], db_info['collection'], str(data['_id']), UPDATE)
    to_send['data'] = data
    dispatcher.send(signal=SIGNAL_UPDATE, sender=to_send)


def trigger_delete(data, db_info, replicated=False):

    if '_id' not in data:
        return no_id_error(DELETE)
    else:
        data['_id'] = str(data['_id'])

    dt = prepare(db_info, DELETE)
    collection = dt[0]
    to_send = dt[1]

    existing_data = collection.find_one({'_id': ObjectId(data['_id'])})
    if not existing_data:
        return no_data_error()

    to_send['data'] = data
    collection.remove(existing_data)
    to_send['log'] = make_log(db_info['db'], db_info['collection'], str(data['_id']), DELETE)
    dispatcher.send(signal=SIGNAL_REMOVE, sender=to_send)


def register_add(callback):
    dispatcher.connect(callback, signal=SIGNAL_ADD, sender=dispatcher.Any)


def register_update(callback):
    dispatcher.connect(callback, signal=SIGNAL_UPDATE, sender=dispatcher.Any)


def register_delete(callback):
    dispatcher.connect(callback, signal=SIGNAL_REMOVE, sender=dispatcher.Any)
