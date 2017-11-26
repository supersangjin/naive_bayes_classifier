from urllib.request import Request, urlopen
import json
from bs4 import BeautifulSoup
import io

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
    grade = row.select(".panel-body > .row > div > .score_table_bottomr > .score_table-bottomr > .score-elem-review > .score_letter-review")[0].text
    load = row.select(".panel-body > .row > div > .score_table_bottomr > .score_table-bottomr > .score-elem-review > .score_letter-review")[1].text
    lecture = row.select(".panel-body > .row > div > .score_table_bottomr > .score_table-bottomr > .score-elem-review > .score_letter-review")[2].text
    comment = ""
    for row in comments:
        comment = comment + row.text + '\n'

    # file.write(title)
    # file.write(prof_year)
    # file.write(comment)
    # file.write(grade + load + lecture)
    # file.write('\n\n\n')

    data_single = {'code': code, 'title': title, 'year': prof_year, 'comment': comment, 'grade': grade, 'load': load,
                   'lecture': lecture}
    data.append(data_single)
f.close()

with io.open('./text_data.txt', 'w', encoding='utf8') as json_file:
    json.dump(data, json_file, ensure_ascii=False)