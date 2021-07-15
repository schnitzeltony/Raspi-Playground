import threading

class ThreadCollectorSingleton():
    instance = None

    def addThread(self, thread):
        ThreadCollectorSingleton.instance.ThreadCollection.append(thread)

    def waitForAllToFinish(self):
        for thread in ThreadCollectorSingleton.instance.ThreadCollection:
            thread.join()

    class __ThreadCollectorHandler:
        def __init__(self):
            self.ThreadCollection = []

    def __init__(self):
        if not ThreadCollectorSingleton.instance:
            ThreadCollectorSingleton.instance = ThreadCollectorSingleton.__ThreadCollectorHandler()

