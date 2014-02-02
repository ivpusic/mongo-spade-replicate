from agents.agent_cache import SENDERS
from bson.json_util import dumps


def on_add(sender):
    data = dumps(sender)
    for s in SENDERS:
        s.replicate_data(data)


def on_update(sender):
    data = dumps(sender)
    print data
    print 'from on_update'
    for s in SENDERS:
        s.replicate_data(data)
