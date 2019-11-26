from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pymysql
import numpy as np
import heapq
from machine_learning.ir_model.config import Config
# import model.config as config
import warnings
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')
import database.dao as dao

import nltk
import math
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
import os
import pickle



# conf = Config()
# stop_words = conf.stop_words
# password = conf.database_password
# database_name = conf.database_name
# print(stop_words)
#
# def get_title():
#     # db = pymysql.connect('localhost', 'root', password=password, database=database_name, charset='utf8')
#     # cursor = db.cursor()
#     # operation = 'select qapair,question_title from questionAndanswer'
#     # cursor.execute(operation)
#
#     text = dao.query_all_qapair_title(dao.connectdb())
#     # db.close()
#     text = np.asarray(text)
#     for index in range(len(text)):
#         text[index][1] = text[index][1].lower()
#     df = pd.DataFrame(np.asarray(text),columns=['qapair','title'])
#     print(df)
#     return df
class inforetrival_model:
    def __init__(self):
        temp=self.cal_tfidfmatrix()
        self.vectorizer=temp[0]
        self.tfidf_mat=temp[1]
        self.df=temp[2]

    def prepocess(self,text):
        def tokenize(text):
            lowers=text.lower()
            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
            no_punctuation = lowers.translate(remove_punctuation_map)
            return nltk.word_tokenize(no_punctuation)

        def del_stoppingword(tokens):
            return [x for x in tokens if not x in stopwords.words('english')]

        def stem_tokens(tokens, stemmer=PorterStemmer()):
            stemmed = []
            for item in tokens:
                stemmed.append(stemmer.stem(item))
            return stemmed

        return ' '.join(stem_tokens(del_stoppingword(tokenize(text))))

        pass

    def cal_tfidfmatrix(self):

        try:
            f=open('ir_data','rb')
            l=pickle.load(f)
            return l
        except:
            print('no that file.')


        text = dao.query_all_qapair_title(dao.connectdb())
        # db.close()
        text = np.asarray(text)
        for index in range(len(text)):
            text[index][1] = self.prepocess(text[index][1])
        df = pd.DataFrame(np.asarray(text), columns=['qapair', 'title'])
        vectorizer = TfidfVectorizer()
        corpus = df.loc[:, 'title']
        tfidf_mat = vectorizer.fit_transform(corpus).toarray()
        wf=open('ir_data','wb')
        data=[vectorizer,tfidf_mat,df]
        pickle.dump(data,wf)
        return data

    def get_the_topNans(self,n,text):


        question_metrix=self.vectorizer.transform([self.prepocess(text)]).toarray()
        matrix = np.dot(self.tfidf_mat, question_metrix.T)
        pair = []
        for i in range(len(matrix)):
            pair.append((i, matrix[i][0]))
        rec_list_for_user = heapq.nlargest(n, dict(pair).items(), key=lambda tup: tup[1])
        return rec_list_for_user

if __name__ == '__main__':
    model=inforetrival_model()
    print(model.prepocess('how to connect mysql with python ?'))
    res=model.get_the_topNans(5,'how to connect pymysql blablabla')
    for each in res:
        temp=model.df.loc[each[0]]
        print(temp.qapair)
    pass

# text = get_title()
# vectorizer = TfidfVectorizer(ngram_range=(1, 2),stop_words=stop_words)
# # vectorizer = TfidfVectorizer(stop_words=stop_words)
# corpus = text.loc[:,'title']
# X = vectorizer.fit_transform(corpus)
# data = X.toarray()
# analyze = vectorizer.build_analyzer()
# # quiz_feature = analyze("How do I use Python's itertools.groupby()?")
# # print(quiz_feature)
# quiz_matrix = vectorizer.transform(["how to connect pymysql"]).toarray()
# print(quiz_matrix)
# print(vectorizer.get_feature_names())
# print(quiz_matrix.shape)
# # user_similarity = cosine_similarity(quiz_matrix,data)
# # print(max(user_similarity[0]))
# # pair = []
# # for i in range(len(user_similarity[0])):
# #     pair.append((i,user_similarity[0][i]))
# # print(pair)
# # rec_list_for_user = heapq.nlargest(3, dict(pair).items(), key=lambda tup: tup[1])
# # print(rec_list_for_user)
# matrix = np.dot(data,quiz_matrix.T)
# pair = []
# for i in range(len(matrix)):
#     pair.append((i,matrix[i][0]))
# print(pair)
# rec_list_for_user = heapq.nlargest(3, dict(pair).items(), key=lambda tup: tup[1])
# for each in rec_list_for_user:
#     print(corpus.loc[each[0]])
