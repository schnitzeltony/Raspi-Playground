import threading

class ThreadCollectorSingleton():
    instance = None

    def addThread(self, thread):
        ThreadCollectorSingleton.instance.ThreadCollection[thread] = ''

    def removeThread(self, thread):
        ThreadCollectorSingleton.instance.ThreadCollection.pop(thread)

    def waitForAllToFinish(self):
        for thread in ThreadCollectorSingleton.instance.ThreadCollection:
            thread.join()

    class __ThreadCollectorHandler:
        def __init__(self):
            self.ThreadCollection = {}

    def __init__(self):
        if not ThreadCollectorSingleton.instance:
            ThreadCollectorSingleton.instance = ThreadCollectorSingleton.__ThreadCollectorHandler()

