import sys
import threading

import nltk.data

from FileProcessor.Boilerplate import HugeProcessor

def init():
    global postTypeId

    postTypeId = "PostTypeId=\""

def checker(line):
    postId = 0;
    try:
        location = line.index(postTypeId) + len(postTypeId)
        postId = int(line[location: location + 1])
    except ValueError:
        pass
    return postId == 1

def consumer(line):
    pass
def producer(list):
    prodLock.acquire()
    list[:] = []
    prodLock.release()

def main(argv):
    init()

   # sent = "Adrian G. Yankov goes to school everyday by bus. he is a very lazy person; however, Roxanne beats him in being lazy."

    #sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    #sents = sent_detector.tokenize(sent.strip())



    smallFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/LimPosts.xml"
    mediumFile = "C:/Users/Nathan/OneDrive/Opleiding/TUe/2IMP25/Assignment 3/MedPosts.xml"
    largeFile = "C:/HUGE/Posts.xml"

    processor = HugeProcessor(checker, consumer, producer, largeFile)

    global prodLock
    prodLock = threading.Lock()

    processor.startProcessing()

if __name__ == "__main__":
    main(sys.argv)

