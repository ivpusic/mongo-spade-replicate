from agents.agent_cache import SENDERS


def on_add(sender):
    SENDERS[0].replicate_data(sender)


def on_update(sender):
    print 'update called...'
