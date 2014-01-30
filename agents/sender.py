import spade
import time


class ReplicationSender(spade.Agent.Agent):

    def send_msg(self, content):
        msg = spade.ACLMessage.ACLMessage()
        msg.setPerformative("inform")
        msg.addReceiver(spade.AID.aid("a@127.0.0.1", ["xmpp://a@127.0.0.1"]))
        msg.setContent('some content')
        msg.setLanguage('english')

        self.send(msg)

    class CheckAndSend(spade.Behaviour.Behaviour):

        def _process(self):
            print 'processing...'
            time.sleep(1)

    def _setup(self):
        p = self.CheckAndSend()
        self.addBehaviour(p, None)
