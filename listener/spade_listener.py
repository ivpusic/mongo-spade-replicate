from agents.agent_cache import SENDERS


def on_add(sender):
    for s in SENDERS:
        s.replicate_data(sender)


def on_update(sender):
    print 'update called...'
