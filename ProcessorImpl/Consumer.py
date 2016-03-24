import threading


class Consumer:
    header = "Score, FavCount, ViewCount, FATs, PoliteTitle, PoliteBody\n"

    def __init__(self):

        self.impolite = open("impolite.csv", "a")
        self.neutral = open("neutral.csv", "a")
        self.polite = open("polite.csv", "a")

        self.lock = threading.Lock()

        self.polite.write(self.header)

        self.neutral.write(self.header)

        self.impolite.write(self.header)

        self.close_all()

    def open_all(self):
        self.impolite = open("impolite.csv", "a")
        self.neutral = open("neutral.csv", "a")
        self.polite = open("polite.csv", "a")


    def store(self, tostore):
        self.lock.acquire()

        self.open_all()

        for item in tostore:

            if item["Polite"] == "Polite":
                self.write_item(item, self.polite)
            elif item["Polite"] == "Neutral":
                self.write_item(item, self.neutral)
            else:
                self.write_item(item, self.impolite)

        tostore[:] = []

        self.polite.flush()
        self.neutral.flush()
        self.impolite.flush()

        self.close_all()

        self.lock.release()

    def close_all(self):
        self.polite.close()
        self.neutral.close()
        self.impolite.close()

    def write_item(self, item, file_to_write):
        line = "{}, {}, {}, {}, {}, {}\n".format(item["Score"], item["FavCount"], item["ViewCount"], item["FATs"],
                                                 item["PolTitle"], item["PolBody"])

        file_to_write.write(line)
