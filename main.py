from event import mongo_event
from listener import spade_listener
from models.test import Person, PersonList
from agents.sender import ReplicationSender
from agents.receiver import ReplicationReceiver
import config


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

    rs = ReplicationSender('{0}_sender@{1}'.format(config.HOST_NAME.lower(), config.HOST_IP), 'secret')
    #rs.start()
    #rs.setDebugToScreen()

    rr = ReplicationReceiver('{0}_receiver@{1}'.format(config.HOST_NAME.lower(), config.HOST_IP), 'secret')
    rr.start()
    rr.setDebugToScreen()
