import spade
import time
import config


class ReplicationSender(spade.Agent.Agent):

    def send_msg(self, content):
        msg = spade.ACLMessage.ACLMessage()
        msg.setPerformative("inform")
        self.rcvr = spade.AID.aid(
            name='{0}@{1}'.format('lubuntu1_receiver', config.HOST_SPADE_IP),
            addresses=['xmpp://{0}@{1}'.format('lununtu1_receiver', config.HOST_SPADE_IP)]
        )

        msg.addReceiver(self.rcvr)
        msg.setContent(content)
        self.send(msg)
        print 'sent...'

    class CheckAndSend(spade.Behaviour.Behaviour):

        def _process(self):
            print 'processing...'
            self.myAgent.send_msg('hello')
            time.sleep(1)

    def _setup(self):
        p = self.CheckAndSend()
        self.addBehaviour(p, None)
