from event.mongo_event import trigger_add
from event.mongo_event import register_add
from listener.spade_listener import on_add
from pymongo import MongoClient
from models.test import Person, PersonList

db = None

def init(db_name):
    client = MongoClient()
    global db
    db = client[db_name]
    register_add(on_add)

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
