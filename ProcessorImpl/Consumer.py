import threading


class Consumer:
    header = "Score, FavCount, ViewCount, FATs, PoliteTitle, PoliteBody\n"

    def __init__(self):

        self.cpp = open("cpp.csv", "a")
        self.python = open("python.csv", "a")

        self.lock = threading.Lock()

        self.cpp.write(self.header)

        self.python.write(self.header)


        self.close_all()

    def open_all(self):
        self.python = open("python.csv", "a")
        self.cpp = open("cpp.csv", "a")


    def store(self, tostore):
        self.lock.acquire()

        self.open_all()

        for item in tostore:

            if item["Language"] == "Both":
                self.write_item(item, self.cpp)
                self.write_item(item, self.python)
            elif item["Language"] == "C++":
                self.write_item(item, self.cpp)
            else:
                self.write_item(item, self.python)

        tostore[:] = []

        self.python.flush()
        self.cpp.flush()

        self.close_all()

        self.lock.release()

    def close_all(self):
        self.cpp.close()
        self.python.close()

    def write_item(self, item, file_to_write):
        line = "{}, {}, {}, {}, {}, {}\n".format(item["Score"], item["FavCount"], item["ViewCount"], item["FATs"],
                                                 item["PolTitle"], item["PolBody"])

        file_to_write.write(line)
