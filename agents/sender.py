import spade
import time


class ReplicationSender(spade.Agent.Agent):

    def send_msg(self, content):
        msg = spade.ACLMessage.ACLMessage()
        msg.setPerformative("inform")
        msg.addReceiver(spade.AID.aid("ivan-virtualbox_receiver@10.24.24.209",
                                      ["xmpp://ivan-virtualbox_receiver@10.24.24.209"]))
        msg.setContent(content)
        self.send(msg)

    class CheckAndSend(spade.Behaviour.Behaviour):

        def _process(self):
            print 'processing...'
            self.myAgent.send_msg('hello')
            time.sleep(1)

    def _setup(self):
        p = self.CheckAndSend()
        self.addBehaviour(p, None)
