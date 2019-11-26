import pymysql
import pickle
import database.data_operation as op
#import data_operation as op

from collections import defaultdict

def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:root, 密码:zh123123
    db = pymysql.connect("18.206.123.67","root","zh123123" ,"comp9900")
    print('连接上了!')
    return db

def query_all_question(db):
    cursor=db.cursor()
    sql1 = "SELECT question_body,answer_body FROM  questionAndanswer"
    try:
        cursor.execute(sql1)
        result=cursor.fetchall()
        closedb(db)

        pass
    except:
        print('crash on query_all_question')

    return result

def query_all_qapair_title(db):
    cursor=db.cursor()
    sql1 = "select qapair,question_title from questionAndanswer"
    try:
        cursor.execute(sql1)
        result=cursor.fetchall()
        closedb(db)

        pass
    except:
        print('crash on query_all_qapair_title')

    return result

# collection commoninf from database
def query_all_commoninf(db):
    cursor=db.cursor()
    sql2="SELECT * FROM commoninf"
    try:
        cursor.execute(sql2)
        result=cursor.fetchall()
        fw = open('commFile','wb')
        pickle.dump(result, fw)
        fw.close()
        pass
    except:
        print('crash on query_all_query_all_commoninf')

def query_of_user(db,course_name,course_number):
    cursor = db.cursor()
    sql = "select * from commoninf where course_name = '{}'or course_number = '{}'".format(course_name,course_number)
    try:
        cursor.execute(sql)
        result1=cursor.fetchall()
        print(result1)
        #closedb(db)


        pass
    except:
        print('Done!')
    return result1

def query_anser_id(db,id):
    cursor = db.cursor()
    sql = f"SELECT answer_body FROM questionAndanswer WHERE qapair='{id}'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    except:
        print("error in query_id")

def query_anser_top(db,id_list):
    cursor = db.cursor()
    res_list=[]
    for id in id_list:
        sql = f"SELECT answer_body FROM questionAndanswer WHERE qapair='{id}'"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            res_list.append(result[0][0])

        except:
            print("error in query_id")
    return res_list

def closedb(db):
    db.close()



if __name__ == '__main__':
    db = connectdb()    # 连接MySQL数据库
    # query_all_commoninf(db)
    # file_name=open('commFile','rb')
    # data=pickle.load(file_name)
    # op.data2csv_comm(data)
    # query_of_user(db,'','COMP9021')
    ans = query_anser_id(db, '150,150')
    print(ans)
