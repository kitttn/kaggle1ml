import re

f = open("../train.csv", encoding="cp1251")
f.readline()


class Data:
    def __init__(self, lst):
        self.postId = lst[0]
        self.postCreationDate = lst[1]
        self.ownerUserId = lst[2]
        self.ownerCreationDate = lst[3]
        self.reputationAtPostCreation = lst[4]
        self.ownerUndeletedAnswerCountAtPostTime = lst[5]
        self.title = lst[6]
        self.bodyMarkdown = lst[7]
        self.tags = lst[8:13]
        self.postClosedDate = lst[13]
        self.openStatus = lst[14]

    def __unicode__(self):
        return "{id: %s}" % self.postId

    def __str__(self):
        return self.__unicode__()


def readOne():
    regexp = r'(?<!")"(?!")'
    fullStr = r'",([a-zA-Z0-9!@#$%^&+*\(\)\[\]\\\/.-]*,){5}(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})*,\d'

    s = f.readline()
    if len(s) == 0:
        return []
    params = s.strip().split(",")

    toTest = '",' + ",".join(params[-7:])
    if re.match(fullStr, toTest):
        # wow, we have a single-line data, good
        return params

    body = "".join(params[7:])[1:]
    params = params[:8]
    while True:
        s = f.readline()
        match = re.search(fullStr, s)
        if match:
            # found end quote, parsing data left
            offs = match.start(0)
            body += s[:offs]
            left = s[offs + 2:]
            params[7] = body
            params += left.strip().split(",")
            return params

        body += s

res = []
while True:
    src = readOne()
    if (len(src) == 0):
        break

    res.append(Data(src))

print(len(res))
