# -*- coding: <utf-8-sig> -*-
import os
import time
import multiprocessing
import threading

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

        # 353 MBs per block
        self.blockSize = 70 * 1000 * 1000
        # Problematic block
        # self.currStart = 2773500000
        self.currStart = 0
        self.currEnd = self.currStart + self.blockSize
        self.blockLock = threading.Lock()

        print("Total filesize is {}".format(self.fileSize))

    def startProcessing(self):
        start = time.clock()

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

            try:
                lines = file.readlines(self.blockSize)

                if self.local.block.start > 0:
                    lines.pop(0)

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

            endTell = file.tell()
            print("Finished block at {}".format(endTell))

            if endTell < self.local.block.end:
                raise "Line missed"

            self.local.block = self.getNextBlock()

    # Method that sets up this thread for processing the file.
    def setup(self):
        if self.props["checkerinthread"]:
            self.local.checker = self.checkercl()
        else:
            self.checker = self.checkercl()
        if self.props["producerinthread"]:
            self.local.producer = self.producercl()
        else:
            self.producer = self.producercl()
        if self.props["consumerinthread"]:
            self.local.consumer = self.consumercl()
        else:
            self.consumer = self.consumercl()

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
