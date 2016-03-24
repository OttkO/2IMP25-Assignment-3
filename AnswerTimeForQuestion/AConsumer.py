import threading


class AnswerTimeConsumer:

    def __init__(self):
        self.lock = threading.Lock()
        self.storage = dict()

    def store(self, to_store):
        self.lock.acquire()

        for item in to_store:

            if item["Question"]:
                hashed_id = hash(item["Id"])
                if hashed_id in self.storage:
                    # If there already is an entry in storage then an answer for this question has been recorded. So
                    # only the question has to be stored.

                    entry = self.storage[hashed_id]
                    entry["QuestionTime"] = item["Time"]
                else:
                    # This question has not been recorded, so it needs to be entered
                    self.storage[hashed_id] = {"QuestionTime": item["Time"]}
            else:
                hashed_id = hash(item["AnswerToId"])
                if hashed_id in self.storage:
                    entry = self.storage[hashed_id]
                    # There can either be a QuestionTime or FastestAnswerTime entry
                    if "FastestAnswerTime" not in entry:
                        entry["FastestAnswerTime"] = item["Time"]
                    else:
                        old_time = entry["FastestAnswerTime"]

                        entry["FastestAnswerTime"] = min(old_time, item["Time"])

                    self.storage[hashed_id] = entry

                else:
                    self.storage[hashed_id] = {"FastestAnswerTime": item["Time"]}

        to_store[:] = []
        self.lock.release()
