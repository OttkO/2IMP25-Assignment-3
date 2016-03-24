class Checker:
    postTypeId = "PostTypeId"
    tags = "Tags"

    def __init__(self):
        pass

    def check(self, line):
        postid = 0
        try:
            postid = int(Checker.getvaluefromxmlattribute(line, self.postTypeId))

            is_q = postid == 1

            if not is_q:
                return False

            tags = Checker.getvaluefromxmlattribute(line, self.tags)

            is_python_or_cpp = "python" in tags or "cpp" in tags or "c++" in tags

            return is_python_or_cpp
        except ValueError:
            return False

    @staticmethod
    def getvaluefromxmlattribute(line, attribute):
        try:
            attribute += "=\""
            startloc = line.index(attribute) + len(attribute)
            endloc = line.index("\"", startloc)
            return line[startloc: endloc]
        except ValueError as ve:
            raise ve
