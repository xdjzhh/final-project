import pymysql
import json
import re


operation = "update questionAndanswer set question_body = '{}' ,answer_body = '{}' where qapair = '{}'"
db = pymysql.connect('localhost', 'root', '666666', 'comp9900', charset='utf8')
cursor = db.cursor()

for file_number in range(0,9):
    with open('right_format{}.json'.format(file_number),'r') as f:
        content = json.load(f)
        for each in content.keys():
            pair = content[each]['question_id'] + ',' + content[each]['answer_id']
            # break
            update = operation.format(pymysql.escape_string(content[each]['title'])
                                      ,pymysql.escape_string(content[each]['answer']),pair)
            try:
                cursor.execute(update)
                db.commit()
            except:
                continue
db.close()