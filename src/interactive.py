import abc


class Interactive(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.trace = False

    def do_trace(self,param):
        self.trace = not self.trace
        print("Trace : {}".format(self.trace))

    @abc.abstractmethod
    def do_in(self, param):
        print("No in command available")
        return

    @abc.abstractmethod
    def do_add(self, param):
        print("No add command available")
        return

    @abc.abstractmethod
    def do_status(self, param):
        print("No status command available")
        return

    @abc.abstractmethod
    def do_go(self, param):
        print("No go command available")
        return