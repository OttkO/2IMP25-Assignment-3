# -*- coding: <utf-8-sig> -*-
import os
import time
import multiprocessing
import threading

import sys

import thread

from random import randint

from FileProcessor.Block import Block


class HugeProcessor:
    local = threading.local()
    tempStorage = 100

    def __init__(self, checkercl, producercl, consumercl,
                 filePath, props):
        self.checkercl = checkercl
        self.consumercl = consumercl
        self.producercl = producercl

        self.checker = None
        self.consumer = None
        self.producer = None

        self.props = props

        self.filePath = filePath
        file = open(filePath)
        self.fileSize = os.fstat(file.fileno()).st_size

        # 32 MBs per block
        self.blockSize = 32 * 1000 * 1000
        # Problematic block
        # self.currStart = 2773500000
        self.currStart = 0
        self.currEnd = self.currStart + self.blockSize
        self.blockLock = threading.Lock()

        print("Total filesize is {}".format(self.fileSize))

    def startProcessing(self):
        start = time.clock()

        if not self.props["checkerinthread"]:
            self.checker = self.checkercl()
        if not self.props["producerinthread"]:
            self.producer = self.producercl()
        if not self.props["consumerinthread"]:
            self.consumer = self.consumercl()

        if "threads" in self.props:
            cores = self.props["threads"]
        else:
            cores = multiprocessing.cpu_count()
        threads = list()

        for i in range(cores):
            t = threading.Thread(target=self.dothreadwork)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        end = time.clock()

        diff = end - start

        print("MBs processed per second is {}, total time was {}".format(int((self.fileSize / diff) / (1000 * 1000)),
                                                                         diff))
        return self.consumer

    def dothreadwork(self):
        self.setup()
        self.partialProcessing()

    def partialProcessing(self):
        # Contains the block this method processes
        self.local.block = self.getNextBlock()

        checker = self.checker
        producer = self.producer
        consumer = self.consumer

        if checker is None:
            checker = self.local.checker
        if producer is None:
            producer = self.local.producer
        if consumer is None:
            consumer = self.local.consumer

        file = open(self.filePath, "rb+")
        store = []

        while self.local.block.start > -1:
            print("Started processing a block that starts at {} and ends at {}".format(self.local.block.start,
                                                                                       self.local.block.end))
            file.seek(self.local.block.start, 0)

            tell = file.tell()
            end_tell = 0

            try:
                lines = file.readlines(self.blockSize)

                if self.local.block.start > 0:
                    rem = lines.pop(0)

                end_tell = file.tell()

                while end_tell - sys.getsizeof(lines[-1]) > self.local.block.end:
                    end_tell -= sys.getsizeof(lines.pop())

                # print "First line processed at {} is {}".format(self.local.block.start, lines[0])
                # print "Last line processed at {} is {}".format(self.local.block.end, lines[-1])

                for line in lines:
                    line = line.decode("utf-8")
                    if checker.check(line):
                        store.append(producer.produce(line))

                    if len(store) > self.tempStorage:
                        consumer.store(store)
            except UnicodeDecodeError as err:
                # If a decode error happens at the start of the line then there is no problem, because
                # the file.seek might put the reader in the middle of a multi-character char.
                if tell != self.local.block.start:
                    raise err

            print("Finished block at {}".format(end_tell))

            if end_tell < self.local.block.end:
                raise "Line missed"

            self.local.block = self.getNextBlock()

        consumer.store(store)

    # Method that sets up this thread for processing the file.
    def setup(self):
        if self.props["checkerinthread"]:
            self.local.checker = self.checkercl()
        if self.props["producerinthread"]:
            self.local.producer = self.producercl()
        if self.props["consumerinthread"]:
            self.local.consumer = self.consumercl()

    def getNextBlock(self):
        self.blockLock.acquire()

        if self.currEnd > self.fileSize:
            self.currEnd = self.fileSize

        block = None

        if self.currStart > self.fileSize:
            self.currStart = -1
            self.currEnd = -1
            block = Block(-1, -1)
        else:
            block = Block(self.currStart, self.currEnd)

        if self.currStart > -1:
            self.currStart += self.blockSize
            self.currEnd += self.blockSize

        self.blockLock.release()

        return block
