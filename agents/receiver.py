import spade


class ReplicationReceiver(spade.Agent.Agent):

    class ReceiveEvent(spade.Behaviour.EventBehaviour):

        def _process(self):
            msg = self._receive().getContent()
            print msg

    def _setup(self):
        self.tmpl = spade.Behaviour.ACLTemplate()
        self.tmpl.setPerformative('inform')
        self.t = spade.Behaviour.MessageTemplate(self.tmpl)

        self.addBehaviour(self.ReceiveEvent(), self.t)
