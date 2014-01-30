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

    li.save()
    p1.save()
