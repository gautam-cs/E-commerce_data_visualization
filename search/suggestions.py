import string
from nltk import sent_tokenize,  word_tokenize
import os
import MyDictionary
from nltk.corpus import stopwords
from neo4j.v1 import GraphDatabase,  basic_auth
driver=GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j",  "password"))
session = driver.session()
stopwords1=set(stopwords.words('english'))

order=['Similar', 'Top', 'Bottom','top','similar','bottom']
Countries=['United Kingdom', 'EIRE', 'Germany', 'France', 'Belgium', 'Portugal', 'Finland', 'Spain', 'Austria',
           'Iceland', 'Cyprus', 'Norway', 'Japan', 'Switzerland', 'Canada', 'Sweden', 'Malta', 'Netherlands',
           'Czech Republic', 'Lithuania', 'Australia', 'Italy', 'Denmark', 'European Community', 'Israel',
           'Singapore', 'Channel Islands', 'Greece', 'RSA', 'USA', 'Bahrain', 'Brazil', 'Poland', 'Lebanon',
           'United Arab Emirates', 'Saudi Arabia']
year=['2010','2011','2012','2013','2014','2015','2016']
Numbers=['5','10']

result1 = []
suggest = []
#x = "match p=(s:start)-[r:by|next*2..3]->() return p;"     # before even user starts typing our list is suggest list
x = "match p=(s:start)-[r:by|in|next*1..2]->() return p;"
result = session.run(x)
for record in result:
    relationships = record["p"].relationships
    nodes = record["p"].nodes
    path = ""
    for i in (range(len(relationships))):
            path += "{0} {1} ".format(nodes[i]["word"],  relationships[i].type)
    path += nodes[-1]["word"]
    result1.append(path)
for ii in result1:
    ii = ii.replace('Start ', '')
    ii = ii.replace('next ', '')
    suggest.append(ii)
#print(result1)
for iii in sorted(suggest, reverse=True):
    print(iii)
#-----------------------------------------------------------------------------------------#

def aftertyping(input):
    print("---------------------inside function---------------------------------------")
    print("'"+input+"'")
    listwsw = []
    listwnsw = []
    last = input.split(' ')[-1]
    if last == '':
        last = input.split(' ')[-2]
    print('last is'+"'"+last+"'")

   
    last=MyDictionary.dictionary(last)
    last=last.split(".")[1]
    if last=="Description":
        last="Products"
    print(last)

    global result1,suggest,result
    result1 = []
    suggest = []
    result = []
    listwsw = input.split(" ")
    print(listwsw)
    for i in listwsw:
        if i not in stopwords1:
            listwnsw.append(i)
    print('listwnsw',listwnsw)

    if last == 'by':
        suggest.append('by')
        xx = "match p=()-[r:by*1]->() return p;"
    elif last=='in':
        suggest.append('in')
        xx = "match p=()-[r:in*1]->() return p;"
    else:
        if last in order:
            xx = 'match p=(c:order{word:"' + last + '"})-[r:in|by|next*1]->() return p;'
        elif last in Countries:
            xx = 'match p=(c:Countries{word:"' + last + '"})-[r:in|by|next*1]->() return p;'
        elif last in Numbers:
            xx = 'match p=(c:Number{word:"' + last + '"})-[r:in|by|next*1]->() return p;'
        else:
            # xx='match p=(c:' + last + ')-[r:in|by|next*1]->() return p;'
            xx = "match p=()-[r:by*1]->() return p;"


    result = session.run(xx)
    for record in result:
        relationships = record["p"].relationships
        nodes = record["p"].nodes
        path = ""
        for i in (range(len(relationships))):
            path += "{1} ".format(nodes[i]["word"], relationships[i].type)
        path += nodes[-1]["word"]
        result1.append(path)
    for ii in result1:
        ii = ii.replace('Start ', '')
        ii = ii.replace('next ', '')
        decide=[]
        decide1=[]
        decide=ii.split(' ')
        for h in decide:
            if h not in stopwords1:
                decide1.append(h)
        if len(set(decide1).intersection(listwnsw))<=0:

             suggest.append(ii)
    # print(result1)

    for iii in set(sorted(suggest, reverse=True)):
        print(iii)

    print("-------------------inside function----------------")
#--------------------------------------------------------------------#

aftertyping('Top location ')
print("-------------SUGGESTIONS----------------------------")
for i in set(sorted(suggest,reverse=True)):
    print(i)
print("-------------SUGGESTIONS------------------------------")
session.close()
