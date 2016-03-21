import sys
import threading

import nltk.data

from FileProcessor.Boilerplate import HugeProcessor
from ProcessorImpl.Checker import Checker
from ProcessorImpl.Consumer import Consumer
from ProcessorImpl.Producer import Producer


def main(argv):



    #sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    #sents = sent_detector.tokenize(sent.strip())

    props = {"checkerinthread": False, "consumerinthread": False, "producerinthread": False}


    smallFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/LimPosts.xml"
    mediumFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/MedPosts.xml"
    largeFile = "C:/HUGE/Posts.xml"

    processor = HugeProcessor(Checker, Producer, Consumer, mediumFile, props)

    processor.startProcessing()

if __name__ == "__main__":
    main(sys.argv)

