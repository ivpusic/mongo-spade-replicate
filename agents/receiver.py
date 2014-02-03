import spade
import config
from event.action import ADD, UPDATE, DELETE
from bson.json_util import loads
from event.mongo_event import trigger_add, trigger_update, trigger_delete
from log.mongo_log import find_log


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

            if 'log' in data:
                sender = message.getSender()
                msg = spade.ACLMessage.ACLMessage()
                msg.setPerformative("inform")
                msg.setOntology('confirm')
                msg.setContent(data['log'])
                msg.addReceiver(sender)
                self.myAgent.send(msg)
            else:
                print 'no log in data!'
                print '#' * 1000

    class ReceivePresence(spade.Behaviour.EventBehaviour):

        def _process(self):
            sender = self._receive().getSender().getName().split('@')[0]
            find_log(sender)

    class OnlineNotify(spade.Behaviour.OneShotBehaviour):

        def _process(self):
            to_send = []
            for key in config.connected:
                agents = [ag[0] for ag in config.connected[key]]
                if self.getAgent().getName().split('@')[0] in agents:
                    to_send.append(key + '_receiver')

            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.setOntology('online')
            msg.setContent('I am online...')
            for agent in to_send:
                self.rcvr = spade.AID.aid(
                    name='{0}@{1}'.format(agent, config.HOST_SPADE_IP),
                    addresses=['xmpp://{0}@{1}'.format(agent, config.HOST_SPADE_IP)]
                )
                msg.addReceiver(self.rcvr)
            self.myAgent.send(msg)

    def _setup(self):
        self.tmpl = spade.Behaviour.ACLTemplate()
        self.tmpl.setPerformative('inform')
        self.tmpl.setOntology('replication')
        self.t = spade.Behaviour.MessageTemplate(self.tmpl)
        self.addBehaviour(self.ReceiveEvent(), self.t)

        self.tmpl = spade.Behaviour.ACLTemplate()
        self.tmpl.setPerformative('inform')
        self.tmpl.setOntology('online')
        self.t = spade.Behaviour.MessageTemplate(self.tmpl)
        self.addBehaviour(self.ReceivePresence(), self.t)

        self.addBehaviour(self.OnlineNotify())
