import dateutil.parser

from ProcessorImpl.Checker import Checker


class LastAnswerTimeProducer:
    post_type_id = "PostTypeId"
    creation_time = "CreationDate"
    id_attr = "Id"
    answer_to_attr = "ParentId"

    def __init__(self):
        pass

    def produce(self, line):
        is_q = int(Checker.getvaluefromxmlattribute(line, self.post_type_id)) == 1
        id = int(Checker.getvaluefromxmlattribute(line, self.id_attr))

        if is_q:
            q_time = Checker.getvaluefromxmlattribute(line, self.creation_time)
            q_time_as_date = dateutil.parser.parse(q_time)
            return {"Question": True, "Id": id, "Time": q_time_as_date}
        else:
            a_time = Checker.getvaluefromxmlattribute(line, self.creation_time)
            a_time_as_date = dateutil.parser.parse(a_time)
            answer_to_id = int(Checker.getvaluefromxmlattribute(line, self.answer_to_attr))
            return {"Question": False, "AnswerToId": answer_to_id, "Time": a_time_as_date}
