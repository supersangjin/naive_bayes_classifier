# -*- coding: utf-8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

f = open("./test_otl.html", 'r')
responseData = f.read()

soup = BeautifulSoup(responseData, "lxml")
targetTableBody = soup.select("#contents > div > div > div.list-group.sort_result")[0]
targetRows = targetTableBody.select("div.panel")
data = []
# with open("crawl_otl.txt", 'w') as file:
for row in targetRows:
    category = row.select(".panel-body > .row > .label-title > h4.ellipsis-content")[0].text
    code = category.split(':')[0].replace(' ', '')
    title = category.split(':')[1].replace(' ', '')
    prof_year = row.select(".panel-body > .row > .label-title > h4.ellipsis-content > small")[0].text
    comments = row.select(".panel-body > .row > .comment > p")
    grade = row.select(
        ".panel-body > .row > div > .score_table_bottomr > .score_table-bottomr > .score-elem-review > .score_letter-review")[
        0].text
    load = row.select(
        ".panel-body > .row > div > .score_table_bottomr > .score_table-bottomr > .score-elem-review > .score_letter-review")[
        1].text
    lecture = row.select(
        ".panel-body > .row > div > .score_table_bottomr > .score_table-bottomr > .score-elem-review > .score_letter-review")[
        2].text
    comment = ""
    for row in comments:
        comment = comment + row.text + '\n'

    # file.write(title)
    # file.write(prof_year)
    # file.write(comment)
    # file.write(grade + load + lecture)
    # file.write('\n\n\n')

    data_single = {"code": code, "title": title, "year": prof_year, "comment": comment, "grade": grade, "load": load,
                   "lecture": lecture}
    data.append(data_single)
# file.close()
f.close()

subjectTrainer = Trainer(tokenizer.Tokenizer(stop_words=[], signs_to_remove=["?!#%&"]))

for subject in data:
    subjectTrainer.train(subject["comment"], subject["grade"])

subjectClassifier = Classifier(subjectTrainer.data, tokenizer.Tokenizer(stop_words=[], signs_to_remove=["?!#%&"]))

unknownInstance = "\n아주 좋은 강의였습니다.\n전자과에서 교과서로 쓰는 ziemer의 통신공학 책은 개인적으로 통신을 처음공부하기에 매우 부적절한 교재라고 생각합니다.\n복잡하고 이해하기 어려운 수식이 매우많아서 수학을 정말정말 잘하는 분이 아니시라면, 이 책 전체를 한학기동안 전부 이해하는 것은 거의 불가능에 가깝다고 생각합니다.\n다행히 교수님께서, 수식보다는 통신에서 필요한 핵심적인 concept들을 중심으로 수업을 진행하셔서, 수식에 매몰되지않고 통신을 잘이해할 수 있었던 것 같습니다.\n\n영어가 아주 유창하시진 않지만, 덕분에 일반적인 한국학생들이 이해하기 좋은 영어를 구사하셔서 수업을 듣기에 어려움이 없었습니다. 질문도 잘 받아주시고, 유머도 있는 편이셔서 수업이 크게 지루하지 않습니다.\n\n과제도 시간을 아주 많이 잡아먹지는 않았습니다만, 너무 벼락치기하면 통수맞을 수 있으니 미리시작하시는 걸 추천합니다.\n\n시험은 평이하게 출제하시는 편이고, 책전부 읽을 필요없이 ppt꼼꼼히 공부하시고 과제 다시 공부하고 하시면 무난하게 득점할 수 있습니다.\n\n학점도 적당히 잘 주신 것 같습니다.\n전반적으로 만족스러운 수업이었습니다.  \n\n\n"
classification = subjectClassifier.classify(unknownInstance)

print(classification)