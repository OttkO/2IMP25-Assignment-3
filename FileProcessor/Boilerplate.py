# -*- coding: <utf-8-sig> -*-
import threading
import os
import time
import multiprocessing
import threading

from FileProcessor.Block import Block


class HugeProcessor:
    local = threading.local()
    tempStorage = 100

    def __init__(self, checker, consumer, producer,
                 filePath):
        self.checker = checker
        self.consumer = consumer
        self.producer = producer

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
        # cores = 1
        threads = list()

        for i in range(cores):
            t = threading.Thread(target=self.partialProcessing)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        end = time.clock()

        diff = end - start

        print("MBs processed per second is {}, total time was {}".format(int((self.fileSize / diff) / (1000 * 1000)),
                                                                         diff))

    def partialProcessing(self):
        # Contains the block this method processes
        self.local.block = self.getNextBlock()

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
                    if self.checker(line):
                        store.append(self.consumer(line))

                    if len(store) > self.tempStorage:
                        self.producer(store)
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
