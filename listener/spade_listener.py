from agents.agent_cache import SENDERS


def on_add(sender):
    for sender in SENDERS:
        sender.replicate_data(sender)


def on_update(sender):
    print 'update called...'
