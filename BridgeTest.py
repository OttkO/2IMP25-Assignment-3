import sys
from jpype import *
import inspect

def main(argv):
    startJVM("C:\\Program Files (x86)\\Java\\jre1.8.0_73\\bin\\client\\jvm.dll", "-ea "
                                            ,"-Djava.class.path=Bridge\\target\\stanfordbridge-1.0-jar-with-dependencies.jar")
    java.lang.System.out.println("hello world")

#I added this code last night after we finished

    brPack = JClass("nl.tue.se.bridge.MainBridge") #finds the class

    bridge = brPack() #calls the constructor

    print bridge.lineToDependencies("Some random words together that form a sentece that says something.") #calls the method with a random sentence, and gets the output as
    #a list which it prints
    #haha awesome, then i will discoard my stuff, h
    #does it work?
    # and you have to shutdown the VM at the end
    shutdownJVM()

if __name__ == "__main__":
    main(sys.argv)