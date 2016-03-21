
class Checker:

    postTypeId = "postTypeId=\""

    def __init__(self):
        pass

    def check(self, line):
        postId = 0
        try:
            location = line.index(self.postTypeId) + len(self.postTypeId)
            postId = int(line[location: location + 1])
        except ValueError:
            pass
        return postId == 1