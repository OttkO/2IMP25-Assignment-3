from ProcessorImpl.Checker import Checker


class TagChecker:
    tags = "Tags"
    post_type_id = "PostTypeId"

    def __init__(self):
        self.encountered = dict()

    def check(self, line):
        try:
            is_q = int(Checker.getvaluefromxmlattribute(line, self.post_type_id)) == 1

            if is_q:
                tags = Checker.getvaluefromxmlattribute(line, self.tags)

                if "python" in tags or "cpp" in tags or "c++" in tags:

                    self.encountered[hash(int(Checker.getvaluefromxmlattribute(line, "Id")))] = True

                    return True

                else:
                    return False

            else:
                answering_id = int(Checker.getvaluefromxmlattribute(line, "ParentId"))

                if hash(answering_id) in self.encountered:
                    return True
                else:
                    return False

        except ValueError:
            return False
