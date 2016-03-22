import threading

import thread
from jpype import JClass, java, attachThreadToJVM


class Producer:
    def __init__(self):
        self.lock = threading.Lock()
        self.id = thread.get_ident()
        attachThreadToJVM()
        print "Contructing instance for {}".format(self.id)
        bridgecl = JClass("nl.tue.se.bridge.MainBridge")
        self.bridge = bridgecl()
        print "Done constructing instance for {}".format(self.id)

    def produce(self, line):

        #get raw text from question and body
        attachThreadToJVM()


        self.lock.acquire()
        #print "getting deps for {}".format(self.id)
        try:
            res = self.bridge.lineToDependencies("This is just a very regular line.")
        except AttributeError as e:
            print self.bridge
            print e
        finally:
            self.lock.release()
        return line