import spade
import json
from event.mongo_event import trigger_add


class ReplicationReceiver(spade.Agent.Agent):

    class ReceiveEvent(spade.Behaviour.EventBehaviour):

        def _process(self):
            data_str = self._receive().getContent()
            print data_str
            print '-'*80
            #data = json.loads(data_str)
            #trigger_add(data['data'], data['db'], replicated=True)

    def _setup(self):
        self.tmpl = spade.Behaviour.ACLTemplate()
        self.tmpl.setPerformative('inform')
        self.tmpl.setOntology('replication')
        self.t = spade.Behaviour.MessageTemplate(self.tmpl)

        self.addBehaviour(self.ReceiveEvent(), self.t)
