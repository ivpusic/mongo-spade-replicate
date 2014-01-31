from event import mongo_event
from listener import spade_listener
from models.test import Person, PersonList
from agents.agent_cache import SENDERS, RECEIVERS


def init():
    mongo_event.register_add(spade_listener.on_add)
    mongo_event.register_update(spade_listener.on_update)

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
