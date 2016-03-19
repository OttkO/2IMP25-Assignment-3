import sys
from jpype import *
import inspect

def main(argv):
    startJVM("C:\\Program Files (x86)\\Java\\jdk1.8.0_73\\jre\\bin\\server\\jvm.dll", "-ea "
                                            ,"-Djava.class.path=Bridge\\target\\stanfordbridge-1.0-jar-with-dependencies.jar")
    java.lang.System.out.println("hello world")

    brPack = JClass("nl.tue.se.bridge.MainBridge")

    bridge = brPack()

    print brPack

    print inspect.getmembers(brPack)


    # and you have to shutdown the VM at the end
    shutdownJVM()

if __name__ == "__main__":
    main(sys.argv)