import re
import json

def sort_json_question():
    with open('q_and_a.json','r') as f:
        lines = json.load(f)
    lines = lines.values()
    data = sorted(lines,key = lambda x:int(x['question_id']))
    print(data)
    return data

def matching(data):
    done = 0
    f = open('content_que.txt','w')
    with open('Posts.xml','r') as file:
        while True:
            line = file.readline()
            if done < 10000:
                if re.search('Id=\"(\d+)\".*PostTypeId=\"1\"',line):
                    index = re.search('Id=\"(\d+)\".*PostTypeId=\"1\"', line).group(1)
                    question_id = data[done]['question_id']
                    # print(index,question_id)
                    if int(index) <= int(question_id):
                        if re.search('Id=\"{}\".*PostTypeId=\"1\"'.format(question_id),line):
                            done += 1
                            print(line)
                            f.write(line)
                    else:
                        done += 1
            else:
                break

            print(done)
    f.close()

def sort_json_answer():
    with open('q_and_a.json','r') as f:
        lines = json.load(f)
    lines = lines.values()
    data = sorted(lines,key = lambda x:int(x['answer_id']))
    print(data)
    return data

def testing(data):
    done = 0
    f = open('content-ans.txt', 'w')
    with open('Posts.xml', 'r') as file:
        while True:
            line = file.readline()
            if done < 10000:
                if re.search('Id=\"(\d+)\".*PostTypeId=\"2\"', line):
                    index = re.search('Id=\"(\d+)\".*PostTypeId=\"2\"', line).group(1)
                    answer_id = data[done]['answer_id']
                    # print(index,answer_id)
                    if int(index) <= int(answer_id):
                        if re.search('Id=\"{}\".*PostTypeId=\"2\"'.format(answer_id), line):
                            done += 1
                            print(line)
                            f.write(line)
                    else:
                        done += 1
            else:
                break

            print(done)
    f.close()

if __name__ == '__main__':
    # data = sort_json_question()
    # matching(data)
    # data = sort_json_answer()
    # testing(data)
    with open('content-ans.txt','r') as f:
        lines = f.readlines()
        print(len(lines))