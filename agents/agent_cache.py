import config
from sender import ReplicationSender
from receiver import ReplicationReceiver

SENDERS = [
    ReplicationSender('{0}_sender@{1}'.format(
        config.HOST_NAME.lower(),
        config.HOST_SPADE_IP), 'secret')
]

RECEIVERS = [
    ReplicationReceiver('{0}_receiver@{1}'.format(
        config.HOST_NAME.lower(),
        config.HOST_SPADE_IP), 'secret')
]
