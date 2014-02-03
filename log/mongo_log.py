from pymongo import MongoClient
from bson.objectid import ObjectId
from event.action import ADD, UPDATE, DELETE
import config
import event

client = MongoClient()
db = client['log']
collection = db['log']


def make_log(db, coll, _id, operation):
    data = {'db': db, 'collection': coll, 'id': _id, 'operation': operation}
    data['agents'] = []
    if config.HOST_NAME in config.connected:
        for agent in config.connected[config.HOST_NAME]:
            data['agents'].append(agent[0])
    for row in collection.find({'id': _id}):
        collection.remove(row)
    return str(collection.insert(data))


def remove_agent_log(agent, log_id):
    for result in collection.find({'_id': ObjectId(log_id)}):
        agents = result['agents']
        if agent in agents:
            agents.remove(agent)
            if not agents:
                collection.remove({'_id': ObjectId(log_id)})
                return True
            collection.update({'_id': result['_id']}, {'$set': {'agents': agents}})
            return True
    return False

client_backup = MongoClient()
db_backup = client['log']
collection_backup = db['log']


def find_log(agent):
    for result in collection.find():
        agents = result['agents']
        if agent in agents:
            _id = result['id']
            db_backup = client[result['db']]
            collection_backup = db_backup[result['collection']]
            action = result['operation']
            db_info = {'collection': result['collection'],
                       'db': result['db']
                       }
            if action == ADD:
                data = collection_backup.find_one({'_id': _id})
                event.mongo_event.trigger_add(data, db_info)
            if action == UPDATE:
                data = collection_backup.find_one({'_id': _id})
                event.mongo_event.trigger_add(data, db_info)
                event.mongo_event.trigger_update(data, db_info)
            if action == DELETE:
                data = {}
                data['_id'] = _id
                event.mongo_event.trigger_delete(data, db_info)
