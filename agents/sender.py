import spade
import config
from log.mongo_log import remove_agent_log


class ReplicationSender(spade.Agent.Agent):

    def send_msg(self, content):
        msg = spade.ACLMessage.ACLMessage()
        msg.setPerformative("inform")
        msg.setOntology('replication')

        ip_addr = config.HOST_NAME
        if ip_addr in config.connected:
            for agent in config.connected[config.HOST_NAME]:
                self.rcvr = spade.AID.aid(
                    name='{0}@{1}'.format(agent[0], agent[1]),
                    addresses=['xmpp://{0}@{1}'.format(agent[0], agent[1])]
                )
                msg.addReceiver(self.rcvr)

            if msg.getReceivers():
                msg.setContent(content)
                self.send(msg)

    class CheckAndSend(spade.Behaviour.OneShotBehaviour):

        def __init__(self, content):
            super(self.__class__, self).__init__()
            self.content = content

        def _process(self):
            self.myAgent.send_msg(self.content)

    class MessageConfirm(spade.Behaviour.EventBehaviour):

        def _process(self):
            content = self._receive()
            log_id = content.getContent()
            agent = content.getSender().getName().split('@')[0]
            remove_agent_log(agent, log_id)
            print 'received!'
            print '*' * 100

    def replicate_data(self, content):
        self.addBehaviour(self.CheckAndSend(content))

    def _setup(self):
        self.tmpl = spade.Behaviour.ACLTemplate()
        self.tmpl.setPerformative('inform')
        self.tmpl.setOntology('confirm')
        self.t = spade.Behaviour.MessageTemplate(self.tmpl)
        self.addBehaviour(self.MessageConfirm(), self.t)
