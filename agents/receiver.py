import spade
from event.action import ADD, UPDATE, DELETE
from bson.json_util import loads
from event.mongo_event import trigger_add, trigger_update, trigger_delete


class ReplicationReceiver(spade.Agent.Agent):

    class ReceiveEvent(spade.Behaviour.EventBehaviour):

        def _process(self):
            message = self._receive()
            data = loads(message.getContent())
            if data['db']['action'] == ADD:
                trigger_add(data['data'], data['db'], replicated=True)
            if data['db']['action'] == UPDATE:
                trigger_update(data['data'], data['db'], replicated=True)
            if data['db']['action'] == DELETE:
                trigger_delete(data['data'], data['db'], replicated=True)

            sender = message.getSender()
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.setOntology('confirm')
            msg.setContent(data['log'])
            msg.addReceiver(sender)
            self.myAgent.send(msg)

    def _setup(self):
        self.tmpl = spade.Behaviour.ACLTemplate()
        self.tmpl.setPerformative('inform')
        self.tmpl.setOntology('replication')
        self.t = spade.Behaviour.MessageTemplate(self.tmpl)
        self.addBehaviour(self.ReceiveEvent(), self.t)
