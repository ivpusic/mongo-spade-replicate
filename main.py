from event import mongo_event
from listener import spade_listener
from models.test import Person, PersonList
from agents.agent_cache import SENDERS, RECEIVERS


def init():
    mongo_event.register_add(spade_listener.on_add)
    mongo_event.register_update(spade_listener.on_update)
    mongo_event.register_delete(spade_listener.on_delete)

    for agent in SENDERS:
        agent.start()
        agent.setDebugToScreen()

    for agent in RECEIVERS:
        agent.start()
        agent.setDebugToScreen()


if __name__ == '__main__':
    init()
    li = PersonList()
    p1 = Person('neki', 'tako')
    p2 = Person('neko', 'nekic')
    li.add(p1)
    li.add(p2)
    li.save()
    p1.save()

    p3 = Person('nn', 'pp', '52edb0daa3d24b1515446077')
    p3.save()
    p3 = Person('nn', 'pp update', '52edb0daa3d24b1515446077')
    p3.update()
    p3.delete()
