import config
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client['log']
collection = db['log']


def make_log(db, coll, _id, operation):
    data = {'db': db, 'collection': coll, 'id': _id, 'operation': operation}
    data['agents'] = []
    if config.HOST_NAME in config.connected:
        for agent in config.connected[config.HOST_NAME]:
            data['agents'].append(agent[0])
    return str(collection.insert(data))


def remove_agent_log(agent, log_id):
    print agent, log_id
    print '*' * 500
    for result in collection.find({'_id': ObjectId(log_id)}):
        agents = result['agents']
        if agent in agents:
            agents.remove(agent)
            collection.update({'_id': result['_id']}, {'$set': {'agents': agents}})
            return True
    return False
