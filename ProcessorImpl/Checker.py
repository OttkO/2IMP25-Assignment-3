class Checker:
    postTypeId = "PostTypeId"
    tags = "Tags"

    def __init__(self):
        pass

    def check(self, line):
        postid = 0
        try:
            postid = int(self.getvaluefromxmlattribute(line, self.postTypeId))

            is_q = postid == 1

            tags = self.getvaluefromxmlattribute(line, self.tags)

            is_python_or_cpp = "python" in tags or "cpp" in tags or "c++" in tags

            return is_q and is_python_or_cpp
        except ValueError:
            return False

    def getvaluefromxmlattribute(self, line, attribute):
        attribute += "=\""
        startloc = line.index(attribute) + len(attribute)
        endloc = line.index("\"", startloc)
        return line[startloc: endloc]
