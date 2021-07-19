import signal
import threading

class AbortSingleton():
    instance = None

    def abortRequested(self):
        return AbortSingleton.instance.exit_event.is_set()

    def requestAbort(self):
        AbortSingleton.instance.exit_event.set()

    class __SignalHandler:
        def __init__(self):
            self.exit_event = threading.Event()
            signal.signal(signal.SIGINT, self.__sigIntHandler)

        def __sigIntHandler(self, signum, frame):
            self.exit_event.set()

    def __init__(self):
        if not AbortSingleton.instance:
            AbortSingleton.instance = AbortSingleton.__SignalHandler()

