import os
import sys
import threading

import gc
from subprocess import call

import nltk.data
import subprocess
from py4j.java_gateway import JavaGateway

from AnswerTimeForQuestion.AConsumer import AnswerTimeConsumer
from AnswerTimeForQuestion.AChecker import TagChecker
from AnswerTimeForQuestion.AProducer import LastAnswerTimeProducer
from FileProcessor.Boilerplate import HugeProcessor
from ProcessorImpl.Checker import Checker
from ProcessorImpl.Consumer import Consumer
import ProcessorImpl.Producer

gateway_running = False


def main(argv):
    largeFile = "C:/Posts.xml"

    props = {"checkerinthread": True, "consumerinthread": False, "producerinthread": True, "threads": 1}

    processor = HugeProcessor(TagChecker, LastAnswerTimeProducer, AnswerTimeConsumer, largeFile, props)

    ProcessorImpl.Producer.answer_time = processor.startProcessing().storage

    processor = None

    gc.collect()

    batch_size = os.stat(largeFile).st_size / float(17)

    start_gateway()

    for i in range(0, 16):
        props = {"checkerinthread": False, "consumerinthread": False, "producerinthread": True,
                 "start": int(batch_size * i), "end": int(batch_size * (i + 1))}
        processor = HugeProcessor(Checker, ProcessorImpl.Producer.Producer, Consumer, largeFile, props)

        processor.startProcessing()

        gc.collect()

        restart_gateway()

    stop_gateway()


def start_gateway():
    global gateway_running
    subprocess.Popen(["java", "-jar", "-Xmx6500m", "Bridge/target/stanfordbridge-1.0-jar-with-dependencies.jar"])
    gateway_running = True


def restart_gateway():
    if gateway_running:
        stop_gateway()

    start_gateway()


def stop_gateway():
    global gateway_running
    JavaGateway().shutdown()
    gateway_running = False


if __name__ == "__main__":
    main(sys.argv)
