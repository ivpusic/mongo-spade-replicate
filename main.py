from event.mongo_event import trigger_add
from event import mongo_event
from listener import spade_listener
from pymongo import MongoClient
from models.test import Person, PersonList

def init(db_name):
    mongo_event.register_add(spade_listener.on_add)
    mongo_event.register_update(spade_listener.on_update)

if __name__ == '__main__':
    init('persons')
    li = PersonList()
    p1 = Person('neki', 'tako')
    p2 = Person('neko', 'nekic')
    li.add(p1)
    li.add(p2)

    li.set_collection('players')
    li.set_db('people')
    li.save()

    p1.set_db('players')
    p1.set_collection('p')
    p1.save()
