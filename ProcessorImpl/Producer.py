import threading

from jpype import JClass


class Producer:
    def __init__(self):
        self.lock = threading.Lock()
        bridgecl = JClass("nl.tue.se.bridge.MainBridge")
        self.bridge = bridgecl()

    def produce(self, line):

        #get raw text from question and body






        self.lock.acquire()
        print self.bridge.lineToDependencies("This is just a very regular line.")
        self.lock.release()
        return line