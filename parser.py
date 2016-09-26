import json
import re


class Data:
    def __init__(self, lst, body):
        self.postId = int(lst[0])
        self.postCreationDate = lst[1]
        self.ownerUserId = int(lst[2])
        self.ownerCreationDate = lst[3]
        self.reputationAtPostCreation = int(lst[4])
        self.ownerUndeletedAnswerCountAtPostTime = int(lst[5])
        self.title = lst[6]
        self.bodyMarkdown = body
        self.tags = lst[7:12]
        self.postClosedDate = lst[12]
        self.openStatus = int(lst[13])

    def __unicode__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.__unicode__()


class Parser:
    def __init__(self, file):
        self.f = file

    def get_title(self, s):
        title_re = r'"((.|\s)*?)"'
        title = ""

        while re.match(title_re, s):
            match = re.match(title_re, s)
            offset = len(match.group())
            title += s[:offset]
            s = s[offset:]

        return title, s

    def read_all(self):
        e = r'",([a-zA-Z0-9!@#$%^&+*\(\)\[\]\\\/.-]*,){5}(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})*,\d'
        body_re = r'"((.|\s)+)"'

        data = []
        full_set = ""

        for s in self.f:
            full_set += s.strip()
            if re.search(e, full_set):
                # print("found a match!")

                split_set = full_set.strip().split(",")
                header = split_set[:6]
                split_set = split_set[6:]
                # print(header)

                title = split_set[0]
                if title.startswith('"'):
                    tmp = ",".join(split_set)
                    title, tmp = self.get_title(tmp)
                    split_set = tmp.split(",")

                # print(title)
                split_set = split_set[1:]

                body = split_set[0]
                if body.startswith('"'):
                    tmp = ",".join(split_set)
                    match = re.match(body_re, tmp)
                    size = len(match.group(0))
                    body = tmp[:size]
                    split_set = tmp[size:].split(",")

                footer = split_set[1:]
                # print(footer)

                element = []
                element.extend(header)
                element.append(title)
                element.extend(footer)

                data.append(Data(element, body))

                full_set = ""

        return data
