import sys
import threading

import nltk.data
from jpype import startJVM, shutdownJVM

from FileProcessor.Boilerplate import HugeProcessor
from ProcessorImpl.Checker import Checker
from ProcessorImpl.Consumer import Consumer
from ProcessorImpl.Producer import Producer


def main(argv):

    startJVM("C:\\Program Files (x86)\\Java\\jre1.8.0_73\\bin\\client\\jvm.dll", "-ea" "-Xmx2200m", "-Xms1024m"
             , "-Djava.class.path=Bridge\\target\\stanfordbridge-1.0-jar-with-dependencies.jar")


    #sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    #sents = sent_detector.tokenize(sent.strip())

    props = {"checkerinthread": False, "consumerinthread": False, "producerinthread": True}


    smallFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/LimPosts.xml"
    mediumFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/MedPosts.xml"
    largeFile = "C:/HUGE/Posts.xml"

    processor = HugeProcessor(Checker, Producer, Consumer, mediumFile, props)

    processor.startProcessing()

    shutdownJVM()

if __name__ == "__main__":
    main(sys.argv)

