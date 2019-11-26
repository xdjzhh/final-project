import pymysql
import json
import re


knowledge_area = 'Information Technology'
with open('data.json','r') as f:
    data = json.load(f)

area_abstract = data[knowledge_area]['abstract']
area_url = data[knowledge_area]['url']

def insert_undergraduate(Undergraduate):
    for course_number in Undergraduate.keys():
        degree = 'Undergraduate'
        course_name = Undergraduate[course_number]['course_name']
        print(course_name)
        course_uoc = Undergraduate[course_number]['course_uoc']
        course_url = Undergraduate[course_number]['course_url']
        course_detail = Undergraduate[course_number]['course_detail']
        course_outline = re.sub('\n','',course_detail['outline'])
        faculty = course_detail['Faculty']
        print(course_number)
        try:
            school = course_detail['School']
        except:
            school = 'None'
        if course_detail['course_term'] != []:
            course_term = course_detail['course_term']
        else:
            course_term = 'None'
        timetable_url = course_detail['timetable_url']
        time_string = 'arrangement:'
        if course_detail['timetable'] != []:
            for each_time in course_detail['timetable']:
                time_string =time_string + each_time + ':' +  course_detail['timetable'][each_time] + ' '
            timetable = time_string
        else:
            timetable = 'None'
        operation = "insert into commoninf(	knowledge_area,area_abstract,area_url,\
                degree,course_number,course_name,course_uoc,course_url,course_outline,\
                faculty,school,course_term,timetable_url,timetable_teacher) values ('{}','{}','{}','{}','{}',\
                '{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(knowledge_area, area_abstract, area_url, \
                         degree, course_number, course_name, course_uoc, course_url, pymysql.escape_string(course_outline), \
                         faculty, school, course_term, timetable_url, pymysql.escape_string(timetable))
        print(operation)
        cursor.execute(operation)
        db.commit()
def insert_postgraduate(Postgraduate):
    for course_number in Postgraduate.keys():
        degree = 'Postgraduate'
        course_name = Postgraduate[course_number]['course_name']
        print(course_name)
        course_uoc = Postgraduate[course_number]['course_uoc']
        course_url = Postgraduate[course_number]['course_url']
        course_detail = Postgraduate[course_number]['course_detail']
        course_outline = re.sub('\n', '', course_detail['outline'])
        faculty = course_detail['Faculty']
        print(course_number)
        try:
            school = course_detail['School']
        except:
            school = 'None'
        if course_detail['course_term'] != []:
            course_term = course_detail['course_term']
        else:
            course_term = 'None'
        timetable_url = course_detail['timetable_url']
        time_string = 'arrangement:'
        if course_detail['timetable'] != []:
            for each_time in course_detail['timetable']:
                time_string = time_string + each_time + ':' + course_detail['timetable'][each_time] + ' '
            timetable = time_string
        else:
            timetable = 'None'
        operation = "insert into commoninf(	knowledge_area,area_abstract,area_url,\
                    degree,course_number,course_name,course_uoc,course_url,course_outline,\
                    faculty,school,course_term,timetable_url,timetable_teacher) values ('{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(knowledge_area, area_abstract, area_url,
                                                                          degree, course_number, course_name, course_uoc,
                                                                          course_url, pymysql.escape_string(course_outline),
                                                                          faculty, school, course_term, timetable_url,
                                                                          pymysql.escape_string(timetable))
        print(operation)
        cursor.execute(operation)
        db.commit()
# db.close()
# cursor.execute('')
def insert_q_a():
    db = pymysql.connect('localhost', 'root', '666666', 'comp9900', charset='utf8')
    cursor = db.cursor()
    degree = 'Postgraduate'
    course_number = 'COMP9021'
    with open('content_que.txt','r') as que:
        que_lines = que.readlines()
    with open('content-ans.txt','r') as ans:
        ans_lines = ans.readlines()

    count = 0
    for each_ans in ans_lines:
        ans_matching = re.search(r'<row Id="(\d+)" PostTypeId="2" ParentId="(\d+)".*Body="(.*&#xA;)".*>',each_ans)
        Id = ans_matching.group(1)
        ParentId = ans_matching.group(2)
        ans_Body = ans_matching.group(3)
        que_and_ans_index = ParentId + ',' + Id
        print(que_and_ans_index)
        for each_que in que_lines:
            if re.search('<row Id="{}".*Body="(.*&#xA;)".*>'.format(ParentId),each_que):
                que_Body = re.search('<row Id="{}".*Body="(.*&#xA;)".*>'.format(ParentId),each_que).group(1)
                count+=1
                print(count)
                print(que_Body)
                operation = "insert into questionAndanswer(qapair,degree,course_number,question_body,answer_body) values \
                ('{}','{}','{}','{}','{}')".format(que_and_ans_index,degree,course_number,pymysql.escape_string(que_Body)
                                                   ,pymysql.escape_string(ans_Body))
                cursor.execute(operation)
                db.commit()
                break
    db.close()

# use comp9900;
# -- create table commoninf(
# -- 	knowledge_area varchar(40),
# --     area_abstract varchar(1000),
# --     area_url varchar(100),
# -- 	degree varchar(40),
# -- 	course_number varchar(40),
# --     course_name varchar(40),
# --     course_uoc varchar(40),
# --     course_url varchar(100),
# --     course_outline varchar(3000),
# -- 	faculty varchar(40),
# --     school varchar(40),
# --     course_term varchar(40),
# --     timetable_url varchar(100),
# --     timetable_teacher varchar(100)
# -- )

if __name__ == '__main__':
    # with open('data.json', 'r') as f:
    #     data = json.load(f)
    #
    # Undergraduate = data[knowledge_area]['Undergraduate']
    # Postgraduate = data[knowledge_area]['Postgraduate']
    # db = pymysql.connect('localhost', 'root', '666666', 'comp9900', charset='utf8')
    #
    # cursor = db.cursor()
    # insert_undergraduate(Undergraduate)
    # insert_postgraduate(Postgraduate)
    # cursor.close()
    insert_q_a()