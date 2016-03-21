class Checker:
    postTypeId = "PostTypeId"

    def __init__(self):
        pass

    def check(self, line):
        postid = 0
        try:
            postid = int(self.getvaluefromxmlattribute(line, self.postTypeId))
        except ValueError:
            pass
        return postid == 1

    def getvaluefromxmlattribute(self, line, attribute):
        attribute += "=\""
        startloc = line.index(attribute) + len(attribute)
        endloc = line.index("\"", startloc)
        return line[startloc: endloc]
