import threading


class Consumer:

    def __init__(self):
        self.lock = threading.Lock()

    def store(self, tostore):
        self.lock.acquire()
        tostore[:] = []
        self.lock.release()
