import sys
import threading

import gc
import nltk.data

from AnswerTimeForQuestion.AConsumer import AnswerTimeConsumer
from AnswerTimeForQuestion.AChecker import TagChecker
from AnswerTimeForQuestion.AProducer import LastAnswerTimeProducer
from FileProcessor.Boilerplate import HugeProcessor
from ProcessorImpl.Checker import Checker
from ProcessorImpl.Consumer import Consumer
import ProcessorImpl.Producer


def main(argv):
    smallFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/LimPosts.xml"
    mediumFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/MedPosts.xml"
    #mediumFile = "C:/HUGE/512Posts.xml"
    largeFile = "C:/HUGE/Posts.xml"

    props = {"checkerinthread": True, "consumerinthread": False, "producerinthread": True, "threads": 1}

    processor = HugeProcessor(TagChecker, LastAnswerTimeProducer, AnswerTimeConsumer, mediumFile, props)

    ProcessorImpl.Producer.answer_time = processor.startProcessing().storage

    processor = None

    gc.collect()

    props = {"checkerinthread": False, "consumerinthread": False, "producerinthread": True}

    processor = HugeProcessor(Checker, ProcessorImpl.Producer.Producer, Consumer, mediumFile, props)

    processor.startProcessing()

if __name__ == "__main__":
    main(sys.argv)

