import sys
from jpype import *
import inspect


def main(argv):
    startJVM("C:\\Program Files (x86)\\Java\\jre1.8.0_73\\bin\\client\\jvm.dll", "-ea "
             , "-Djava.class.path=Bridge\\target\\stanfordbridge-1.0-jar-with-dependencies.jar")
    java.lang.System.out.println("hello world")

    brPack = JClass("nl.tue.se.bridge.MainBridge")

    bridge = brPack()

    print bridge.lineToDependencies(
        "Some random words together that form a sentece that says something.")
    shutdownJVM()


if __name__ == "__main__":
    main(sys.argv)
