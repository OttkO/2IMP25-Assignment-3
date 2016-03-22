import sys
import threading

from jpype import *
import inspect


def main(argv):
    startJVM("C:\\Program Files (x86)\\Java\\jre1.8.0_73\\bin\\client\\jvm.dll", "-Xmx1024m"
             , "-Djava.class.path=Bridge\\target\\stanfordbridge-1.0-jar-with-dependencies.jar")
    java.lang.System.out.println("hello world")

    brPack = JClass("nl.tue.se.bridge.MainBridge")

    global bridge
    bridge = brPack()

    print bridge.lineToDependencies(
        "Some random words together that form a sentence that says something.")
    t = threading.Thread(target=loopSents)
   # t.start()

    loopSents()
    shutdownJVM()


def loopSents():
    while True:
        print bridge.lineToDependencies("Some random words together that form a sentece that says something.")

if __name__ == "__main__":
    main(sys.argv)
