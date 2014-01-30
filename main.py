from event import mongo_event
from listener import spade_listener
from models.test import Person, PersonList
from agents.sender import ReplicationSender


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

    rs = ReplicationSender('replica_send@10.24.20.61', 'secret')
    rs.start()
