import spade
import config
from network import ip


class ReplicationSender(spade.Agent.Agent):

    def send_msg(self, content):
        msg = spade.ACLMessage.ACLMessage()
        msg.setPerformative("inform")

        for agent in config.connected[ip.get_lan_ip()]:
            self.rcvr = spade.AID.aid(
                name='{0}@{1}'.format(agent[0], agent[1]),
                addresses=['xmpp://{0}@{1}'.format(agent[0], agent[1])]
            )
            msg.addReceiver(self.rcvr)

        if msg.getReceivers():
            msg.setContent(content)
            self.send(msg)
            print 'sent...'

    class CheckAndSend(spade.Behaviour.OneShotBehaviour):

        def __init__(self, content):
            super(self.__class__, self).__init__()
            self.content = content

        def _process(self):
            self.myAgent.send_msg(self.content)

    def replicate_data(self, content):
        self.addBehaviour(self.CheckAndSend(content))

    def _setup(self):
        pass
