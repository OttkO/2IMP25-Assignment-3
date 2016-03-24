import HTMLParser
import threading
from bs4 import BeautifulSoup
from py4j.java_gateway import JavaGateway

from Dep import model
import thread

import nltk

from ProcessorImpl.Checker import Checker

global locky
answer_time = None
locky = threading.Lock()


class Producer:
    title_attr = "Title"
    body_attr = "Body"
    fav_count_attr = "FavoriteCount"
    view_count_attr = "ViewCount"
    score_count_attr = "Score"

    def __init__(self):
        self.lock = threading.Lock()
        self.id = thread.get_ident()
        gateway = JavaGateway()

        self.bridge = gateway.entry_point.getBridge()
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


    def produce(self, line):

        q_id = int(Checker.getvaluefromxmlattribute(line, "Id"))

        title = Checker.getvaluefromxmlattribute(line, self.title_attr)
        body = self.raw_text_from_body(Checker.getvaluefromxmlattribute(line, self.body_attr))

        # Because the stackoverflow data dump is weird.
        if self.fav_count_attr in line:
            fav_count = int(Checker.getvaluefromxmlattribute(line, self.fav_count_attr))
        else:
            fav_count = 0
        view_count = int(Checker.getvaluefromxmlattribute(line, self.view_count_attr))
        score_count = int(Checker.getvaluefromxmlattribute(line, self.score_count_attr))

        title_pol = self.politeness_for_block(title)
        body_pol = self.politeness_for_block(body)

        answer_time_entry = answer_time[hash(q_id)]

        if "FastestAnswerTime" not in answer_time_entry:
            fastest_answer_time_sec = -1
        else:
            fastest_answer_time_sec = (answer_time_entry["FastestAnswerTime"] - answer_time_entry["QuestionTime"]).total_seconds()

        tags = Checker.getvaluefromxmlattribute(line, "Tags")

        if "python" in tags and ("cpp" in tags or "c++" in tags):
            language = "Both"
        elif "Python" in tags:
            language = "Python"
        else:
            language = "C++"

        return {"Score": score_count, "FavCount": fav_count, "ViewCount": view_count, "FATs": fastest_answer_time_sec,
                "PolTitle": title_pol, "PolBody": body_pol, "Language": language}

    def politeness_for_block(self, block):
        block_sentences = self.sentence_tokenizer.tokenize(block.strip())

        block_res = list()
        for sent in block_sentences:
            sent_deps = self.bridge.lineToDependencies(sent)
            sent_deps_plist = list()

            for i in range(sent_deps.size()):
                sent_deps_plist.append(sent_deps.get(i))

            block_res.append(sent_deps_plist)

        title_pol_requests = {"sentences": block_sentences, "parses": block_res}

        return model.score(title_pol_requests)["polite"]

    def raw_text_from_body(self, body):
        html_parser = HTMLParser.HTMLParser()
        unescaped = html_parser.unescape(body)

        soup = BeautifulSoup(unescaped, "lxml")

        [s.extract() for s in soup("pre")]
        [s.extract() for s in soup("code")]

        return soup.get_text()
