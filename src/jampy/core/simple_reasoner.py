import _thread

# TODO : situation calclus, and command to executor
class SimpleReasoner:
    rule_list = []

    def start(self):
        _thread.start_new_thread(self.run,())

    def run(self):
        pass

    def add_rule(self, rule_callback):
        pass