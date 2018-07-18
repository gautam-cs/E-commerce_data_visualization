import csv
import os
import re
import pandas as pd
from django.shortcuts import render, redirect
from chatterbot import ChatBot
from . import MyDictionary,hasproductname
from nltk.tag import StanfordNERTagger
from nltk.corpus import stopwords, state_union, wordnet
from nltk import sent_tokenize, word_tokenize
import random
from collections import Counter
import pandas as pd
from sklearn import tree
import numpy as np
import pydotplus
import os
from sklearn.externals.six import StringIO
from nltk.corpus import stopwords
from collections import Counter
from neo4j.v1 import GraphDatabase, basic_auth
from django.contrib.staticfiles.templatetags.staticfiles import static
base_dir= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""change according to the IP in which Neo4j server is running, by default it is set to local system""" 
# driver = GraphDatabase.driver("bolt://10.141.63.61:7687", auth=basic_auth("neo4j", "password"))
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "password"))
session = driver.session()
os.environ["PATH"] += os.pathsep + os.path.join(base_dir , 'search/static/packages/graphviz-2.38/release/bin')
productslist=[]
customerslist=[]
ages=[]
category=[]
totalspent=[]
pricesensi=[]
most_buyed_item_cost=[]
actualcategoryspresent=[]
starts=[]
ends=[]
cat=[]
bucketsizes=[]
countryofcustomer=[]



stanford_classifier=os.path.join(base_dir , 'search/static/packages/stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz')
stanford_ner_path=os.path.join(base_dir , "search/static/packages/stanford-ner-2016-10-31/stanford-ner.jar")

#set the path of jre/bin/java.jre as per the path of file installed in your system.
# java_path = "C:\Program Files\Java\jre1.8.0_101/bin/java.exe"
# os.environ['JAVAHOME'] = java_path
os.environ['JAVAHOME']=os.path.join(base_dir , "search\static\packages\jre1.8.0_101/bin/java.exe")
productname=stanford_ner_path
def statement(query):
    st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
    tokenized_text = word_tokenize(query)
    tokenized_list=[]
    for i in tokenized_text:
        tokenized_list.append(i.lower())
    print('tokened list= ',tokenized_list)
    replacedlist=[]
    for j in tokenized_list:
        dictionary_value=MyDictionary.chat_dict(j)
        if  dictionary_value != None:
            replacedlist.append(dictionary_value)
        else:
            replacedlist.append(j)

    print("replaced list",replacedlist)
    classified_text = st.tag(replacedlist)
    print("tagging=",classified_text)
    classified_text=dict(classified_text)
    dict_loc=" "
    value=""
    input_statement=query
    print("###################replacedlist",replacedlist)
    temp=''
    for i in (replacedlist):
        prev=temp +" " +i
        temp=i
        print("safdcrsdv",prev,temp)
        if i=="location":
            dict_loc="LOCATION"
        elif i=="top":
            value="top"
        elif i=="bottom":
            value="bottom"
        elif i=="similar":
            value="similar"
        elif i=="Help":
            value="Help"
        elif i=="trend":
            value="trend"
        elif i=="segment" or prev=="who buys":
            value="segment"
    print("#######################value",value,dict_loc)

    if( value=="top"):
        input_statement="top product"
        if (dict_loc=="LOCATION" ):  
            input_statement=input_statement + ' in country'
        elif(value=="trend"):
            input_statement="trend"
    elif(value=="bottom"):  
        input_statement="bottom product"
        if(dict_loc=="location"):
            input_statement=input_statement + " in country"
        elif (value == "trend"):
            input_statement = "trend"
    elif(value=="trend"):
        input_statement="trend of the product"
    elif(value=="segment"):
        input_statement="segment of product"
    elif(value=="Help"):
        input_statement="Help me"
    return input_statement


def home(request):
    if request.method=="POST":
        query=request.POST['query']
        #----------------------------chatbot Part--------------------------------#
        #---------------------file training on dataset---------------------------#

        """For training the module according to required json file must be kept in your system 
        in the directory chatterbot_corpus\data\(language you want to train in)
        training file is availabe in staic/chatbot_traing just place it in above mention directory"""

        # chatbot = ChatBot(
        #         "Terminal",
        #         trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
        
        # chatbot.train("chatterbot.corpus.english.module")
        # chatbot.train("chatterbot.corpus.english.greetings")

        #------------------------------------------------------------------------#
        input_statement=statement(query) 
        print("input statement",input_statement)

        chatbot = ChatBot(
        "Terminal",
                storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
                logic_adapters=[{
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help me',
            'output_text': 'Ok, go to sample queries'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        },
        ],
                input_adapter="chatterbot.input.VariableInputTypeAdapter",
                output_adapter="chatterbot.output.OutputAdapter",
                database="database.db"
                )
        bot_output = chatbot.get_response(input_statement)
        print("##########################bot_output",bot_output)
        if bot_output=="top":
            column_list_length=(query_and_nlp(bot_output,query))
            if (column_list_length==2):
                return redirect('/graph_bar_2')

            elif(column_list_length==3):
                return redirect('/graph_bar_3')

            else:
                return redirect('/error_page')
        elif bot_output=="bottom":
            column_list_length=(query_and_nlp(bot_output,query))
            if (column_list_length==2):
                return redirect('/graph_bar_2')

            elif(column_list_length==3):
                return redirect('/graph_bar_3')

            else:
                return redirect('/error_page')
        elif bot_output=="trend":
            column_list_length=(query_and_nlp(bot_output,query))
            if (column_list_length==2):
                return redirect('/trend_2')

            elif(column_list_length==3):
                return redirect('/trend_3')
        elif bot_output=="segment":
            column_list_length=query_and_nlp(bot_output,query)
            return redirect('/segment')
        else :
            print(bot_output)
            return render(request,'index.html',{"bot_output":bot_output,"input_statement":input_statement})
        print(bot_output)

    else:
        with open(os.path.join(base_dir , "search/static/data/finaldataset.csv"), newline='') as f:
            df = pd.read_csv(f)
            columns = df.columns
            list1 = []
            for i in range(len(columns)):
                list1.append(columns[i])
        list2=["for 12359","for 12408","for 12562","for 12683","for 12783","for 12955","for 13588","for 14261",
               "for 15532","for 16549","for 16918","for 17511","top","products by margin","products by reverue",
               "products by location","of DOLLY GIRL BEAKER","of NINE DRAWER OFFICE TIDY","of RED SPOT GIFT BAG LARGE",
               "of OVAL WALL MIRROR DIAMANTE","of DOLLY BOY BEAKER","of 4 PURPLE FLOCK DINNER CANDLES",
               "of 5 PURPLE FLOCK DINNER CANDLES","of SQUARE WALL MIRROR DIAMANTE","of DOLLY MEN BEAKER",
               "of DOLLY WOMEN BEAKER","of YELLOW SPOT GIFT BAG LARGE","of I LOVE LONDON MAXI BACKPACK",
               "buys RED SPOT GIFT BAG LARGE","buys OVAL WALL MIRROR DIAMANTE","buys DOLLY BOY BEAKER",
               "buys 4 PURPLE FLOCK DINNER CANDLES","buys 5 PURPLE FLOCK DINNER CANDLES",
               "buys SQUARE WALL MIRROR DIAMANTE","buys DOLLY MEN BEAKER","buys DOLLY WOMEN BEAKER",
               "buys YELLOW SPOT GIFT BAG LARGE"]
        list=list1+list2
        return render(request, 'index.html',{'list':list})


#-------------------------------------------Top Bottom function-------------------------------------------------------------#
def top_bottom(replacedlist,replacedlistwithnodot,replacedlistwithnos,where1,function_call):
    print("function call",function_call)
    print('replacedlist',replacedlist)
    print('replacedlistwithnodot',replacedlistwithnodot)
    print('replacedlistwithnos',replacedlistwithnos)
    A = ['Description', 'Country', 'CustomerID','Gender','Category']
    B = ['Quantity', 'revenue']
    C = ['Price']
    A1=[]
    A1dot=[]
    B1=[]
    B1dot=[]
    C1=[]
    C1dot=[]
    for i in replacedlist:
        if i[2:] in A:
            A1dot.append(i)
            A1.append(i[2:])
        if i[2:] in B:
            B1dot.append(i)
            B1.append(i[2:])
        if i[2:] in C:
            C1dot.append(i)
            C1.append(i[2:])
    print('A1 =',A1)
    print('B1 =',B1)
    print('C1 =', C1)
    B1C1=B1+C1
    B1dotC1dot=B1dot+C1dot
    print('A1dot =', A1dot)
    print('B1dot =', B1dot)
    print('C1dot =', C1dot)
    ########MATCH######################################################################################
    match = 'match (c:customerid)-[r:Bought_this]->(s:stockcode)'
    ########SET#########################################################################################
    set1 = 'set r.Quantity=toInteger(r.Quantity),r.Price=toFloat(r.Price),r.revenue =toFloat(r.revenue)'
    ########RETURN######################################################################################
    returns = 'return '
    if 'Description' in A1 and len(C1) != 0:
            returns =returns+ ' Distinct '
    for iii in range(0, len(A1)):
        if iii != 0:
            returns = returns + ' ,' + A1dot[iii] + ' as ' + A1[iii] + ' '
        else:
            returns = returns + '  ' + A1dot[iii] + ' as ' + A1[iii] + ' '
    ########ORDER BY###################################################################################
    orderby = 'order by '
    descc = 'DESC'
    if function_call=="top":
        descc = 'DESC'
    else:
        descc=''
    if len(B1C1)<=1 and len(A1)<=2:
        if 'Description' in A1:
            if len(B1C1) == 0:
                returns = returns + ', reduce(sum=0,i in collect(r.revenue)|sum+i) as revenue'
                orderby = 'order by revenue  ' + descc + ' '
            else:
                returns = returns + ', reduce(sum=0,i in collect(' + B1dotC1dot[0] + ')|sum+i) as ' + B1C1[0]
                orderby = 'order by ' + B1C1[0] + ' ' + descc + ' '
            ##########################################CUSTOMERS#################################################
        else:
            if 'CustomerID' in replacedlistwithnodot:
                if len(B1C1) == 0:
                    returns = returns + ', reduce(sum=0,i in collect(r.revenue)|sum+i) as revenue'
                    orderby = 'order by revenue  ' + descc + ' '
                else:
                    returns = returns + ', reduce(sum=0,i in collect(' + B1dotC1dot[0] + ')|sum+i) as ' + B1C1[0]
                    orderby = 'order by ' + B1C1[0] + ' ' + descc + ' '
            else:
                if 'Country' in replacedlistwithnodot:
                    if len(B1C1) == 0:
                        returns = returns + ', reduce(sum=0,i in collect(r.revenue)|sum+i) as revenue'
                        orderby = 'order by revenue  ' + descc + ' '
                    else:
                        returns = returns + ', reduce(sum=0,i in collect(' + B1dotC1dot[0] + ')|sum+i) as ' + B1C1[0]
                        orderby = 'order by ' + B1C1[0] + ' ' + descc + ' '
                if 'Country' not in replacedlistwithnodot:
                    print('errorno = 1')
                    print('Type something meaningfull....')
                    #exit()
    else:
        print('Write something meaningfull')
        exit(code=True)
    if where1=='where ':
        where1=''
    print(match)
    print(where1)
    print(set1)
    print(returns)
    print(orderby)
    x = match + ' ' + where1 + ' ' + set1 + ' ' + returns + ' ' + orderby + ' ' + ' '
    print("top_bottom",x)
    col_length=get_result(x)
    return col_length


def trend(replacedlist,replacedlistwithnodot,replacedlistwithnos,productname,year1,where1):
    print('%%%%%%%%%%%%%%%%%%%%%')

    if productname is None:
        print('please enter a product')
        # exit()
    print('Showing trends for product',"'"+str(productname)+"'")
    print('replacedlist', replacedlist)
    print('replacedlistwithnodot', replacedlistwithnodot)
    print('replacedlistwithnos', replacedlistwithnos)
    A = ['Description', 'Country', 'CustomerID', 'Gender','Category']
    B = ['Quantity', 'revenue']
    C = ['Price']
    A1 = []
    A1dot = []
    B1 = []
    B1dot = []
    C1 = []
    C1dot = []
    for i in replacedlist:
        if i[2:] in A:
            A1dot.append(i)
            A1.append(i[2:])
        if i[2:] in B:
            B1dot.append(i)
            B1.append(i[2:])
        if i[2:] in C:
            C1dot.append(i)
            C1.append(i[2:])
    print('A1 =', A1)
    print('B1 =', B1)
    print('C1 =', C1)
    B1C1 = B1 + C1
    B1dotC1dot = B1dot + C1dot
    print('A1dot =', A1dot)
    print('B1dot =', B1dot)
    print('C1dot =', C1dot)
    print(productname)
    if where1=='where ':
        if len(year1)==1:
            where1=where1+' s.Description='+"'"+productname+"' and tointeger(r.Year)<="+year1[0]
            print(where1)
        elif len(year1)==2:
            where1=where1+' s.Description='+"'"+productname+"' and tointeger(r.Year)>="+year1[0]+' and tointeger(r.Year)<='+year1[1]
            print(where1)
        else:
            if productname is not None:
                where1 = 'where s.Description=' + "'" + productname + "'"
            else:
                where1=''
    elif where1!='where ':
        if len(year1)==1:
            where1=where1+' and s.Description='+"'"+productname+"' and tointeger(r.Year)<="+year1[0]
            print(where1)
        elif len(year1)==2:
            where1=where1+' and s.Description='+"'"+productname+"' and tointeger(r.Year)>="+year1[0]+' and tointeger(r.Year)<='+year1[1]
            print(where1)
        else:
            where1=where1+' and s.Description='+"'"+productname+"'"

    match='match(c:customerid)-[r:Bought_this]->(s:stockcode)'
    set1='set r.Quantity = toInteger(r.Quantity), r.Price = toFloat(r.Price), r.revenue = toFloat(r.revenue)'
    if productname is not None:
        if 'Country' in A1:
            returns='return r.Year as Year, c.Country as Country,reduce(sum=0, i in collect(r.Quantity) | sum + i) as Quantity'
        else:
            returns='return r.Year as Year, reduce(sum=0, i in collect(r.Quantity) | sum + i) as Quantity'
    else:

        returns = 'return r.Year as Year,s.Description as description , reduce(sum=0, i in collect(r.Quantity) | sum + i) as Quantity'
    orderby='order by r.Year'
    print(match)
    print(where1)
    print(set1)
    print(returns)
    print(orderby)
    x = match + ' ' + where1 + ' ' + set1 + ' ' + returns + ' ' + orderby + ' ' + ' '
    print("xxxx",x)
    col_length=get_result(x)
    return col_length


def get_result(x):
    session = driver.session()
    result = session.run(x)
    column_list=[]
    for i in result:
        column_list = i.keys()
        break
    csvfile  = open(os.path.join(base_dir , 'search/static/data/converted_data.csv'), 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(column_list)
    for i in result:
        val = []
        for keys in column_list:
            val.append(i[keys])
        writer.writerow(val)
    csvfile.close()
    session.close()
    return len(column_list)    


def segemnt(productname,productslist,customerid,customerslist):

    target=[]
##################################################################################################
    def Most_Common(lst):
        data = Counter(lst)
        return data.most_common(1)[0][0]
    def price_bucket_of_product(start,end,bucketsize,value):
        start=float(start)
        end = float(end)
        bucketsize = float(bucketsize)
        value = float(value)
        if value>=start and value<=start+2*bucketsize:
            # return random.uniform(0.76, 1)
            return 'Low'
        if value >= start+2*bucketsize and value <= start + 5 * bucketsize:
            # return random.uniform(0.51, 0.75)
            return 'Medium Low'
        if value >= start + 5 * bucketsize and value <= start + 8 * bucketsize:
            # return random.uniform(0.26, 0.5)
            return 'Medium High'
        if value >= start + 8 * bucketsize and value <= end:
            # return random.uniform(0,0.25)
            return 'High'
    def drop_in_bucket(start,end,bucketsize,value):
        start=float(start)
        end = float(end)
        bucketsize = float(bucketsize)
        value = float(value)
        if value>=start and value<=start+2*bucketsize:
            # return random.uniform(0.76, 1)
            return 'High'
        if value >= start+2*bucketsize and value <= start + 5 * bucketsize:
            # return random.uniform(0.51, 0.75)
            return 'Medium High'
        if value >= start + 5 * bucketsize and value <= start + 8 * bucketsize:
            # return random.uniform(0.26, 0.5)
            return 'Medium Low'
        if value >= start + 8 * bucketsize and value <= end:
            # return random.uniform(0,0.25)
            return 'Low'

    def ageassign(pricesensi):
        global ages
        for i in pricesensi:
            if i=='High':
                ages.append(random.randint(15,20))
            elif i=='Medium High':
                dec=random.randint(1,2)
                if dec==1:
                    ages.append(random.randint(20,30))
                else:
                    ages.append(random.randint(60,80))
            elif i=='Medium Low':
                ages.append(random.randint(31,40))
            elif i=='Low':
                ages.append(random.randint(41,50))


    def product_segment(productslist,customerid):
        descriptions=[]
        mrp=[]
        categoryofproduct=[]
        yes_no=[]
        cat=[]
        xx='match(c:customerid)-[r:Bought_this]->(s:stockcode) ' \
           'set r.Actual_Price=toFloat(r.Actual_Price)' \
           'return s.Category,collect(DISTINCT r.Actual_Price) as pricelist ' \
           'order by s.Category, pricelist'
        pricebucket=session.run(xx)

        for i in pricebucket:
            # print(i)
            actualcategoryspresent.append(i['s.Category'])
            if len(i['pricelist'])==1:
                start=(i['pricelist'][0])-1
                end=(i['pricelist'][0])+1
            else:
                start = min(i['pricelist'])
                end = max(i['pricelist'])

            bucketsize=(end-start)/10
            starts.append(start)
            ends.append(end)
            bucketsizes.append(bucketsize)
            cat.append(i['s.Category'])
            # print('start      :',start)
            # print('end        :',end)
            # print('bucket_size:',bucketsize)

        for i in productslist:
            x='match() - [r:Bought_this]->(s:stockcode{StockCode:"'+i+'"}) ' \
              'return distinct s.Description as description, s.Category as category, r.Actual_Price as MRP ' \
              'limit 1'
            result=session.run(x)
            for i in result:
                descriptions.append(i['description'])
                mrp.append(i['MRP'])
                categoryofproduct.append(i['category'])
        df1 = pd.DataFrame(columns=['Description', 'MRP', 'category', 'PriceBucket'])
        for i in productslist:
            x = 'optional MATCH(c:customerid{CustomerID: "' + customerid + '"})-[r:Bought_this]->(s:stockcode{StockCode: "' + i + '"}) ' \
                'return distinct ' \
                'case ' \
                'when r.Quantity IS NULL THEN 0 ' \
                'when r.Quantity IS NOT NULL THEN 1 ' \
                'else r.Quantity END AS Quantity '
            for ii in session.run(x):
                yes_no.append(ii[0])
        for i in range(0,len(productslist)):
            # print('=======================================================================================================')
            # print('StockCode of product                             :',productslist[i])
            # print('Description of product                           :',descriptions[i])
            # print('MRP                                              :',mrp[i])
            # print('Category of product                              :',categoryofproduct[i])
            # if categoryofproduct[i] in cat:
            vv = cat.index(categoryofproduct[i])
            z=price_bucket_of_product(starts[vv], ends[vv], bucketsizes[vv],mrp[i])
            # print('Price bucket                                     :',z)
            # print('yes_no                                           :',yes_no[i])

            df1 = df1.append({'Description': descriptions[i], 'MRP': mrp[i], 'category': categoryofproduct[i], 'PriceBucket': z},ignore_index=True)


        # hot_descp = pd.get_dummies(df1.Description)
        # df1 = df1.join(hot_descp)
        df1 = df1.drop('Description', axis=1)

        hot_category = pd.get_dummies(df1.category)
        df1 = df1.join(hot_category)
        df1 = df1.drop('category', axis=1)

        hot_PriceBucket = pd.get_dummies(df1.PriceBucket)
        df1 = df1.join(hot_PriceBucket)
        df1 = df1.drop('PriceBucket', axis=1)
        # print(df1)
        data = df1.values
        train_target = yes_no
        train_data = data
        # print(train_target)
        # print(train_data)


        x = tree.DecisionTreeClassifier()

        x.fit(train_data, train_target)
        # print(x)
        dot_data = StringIO()
        tree.export_graphviz(x, out_file=dot_data, feature_names=df1.columns.tolist(), class_names=['No', 'Yes'],
                             filled=True, rounded=True, impurity=False)

        for i in dot_data:
            print(i)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

        graph.write_png('D:\project\search\static\stuff/segment.png')

    def customer_segment(customerslist,productname):
        g=globals()



        xx='match(c:customerid)-[r:Bought_this]->(s:stockcode) ' \
           'set r.Actual_Price=toFloat(r.Actual_Price)' \
           'return s.Category,collect(DISTINCT r.Actual_Price) as pricelist ' \
           'order by s.Category, pricelist'
        pricebucket=session.run(xx)

        for i in pricebucket:
            # print(i)
            actualcategoryspresent.append(i['s.Category'])
            if len(i['pricelist'])==1:
                start=(i['pricelist'][0])-1
                end=(i['pricelist'][0])+1
            else:
                start = min(i['pricelist'])
                end = max(i['pricelist'])

            bucketsize=(end-start)/10
            starts.append(start)
            ends.append(end)
            bucketsizes.append(bucketsize)
            cat.append(i['s.Category'])
            # print('start      :',start)
            # print('end        :',end)
            # print('bucket_size:',bucketsize)
        for i in customerslist:
            x = 'optional MATCH(c:customerid{CustomerID: "' + i + '"})-[r:Bought_this]->(s:stockcode{Description: "' + productname + '"}) ' \
                 'return distinct ' \
                 'case ' \
                 'when r.Quantity IS NULL THEN 0 ' \
                 'when r.Quantity IS NOT NULL THEN 1 ' \
                 'else r.Quantity END AS Quantity '
            for ii in session.run(x):
                target.append(ii[0])
        for i in customerslist:
            x='match(c1:customerid{CustomerID: "'+i+'"})-[r1:Bought_this]->(s1:stockcode) return c1.Country limit 1'
            result=session.run(x)
            for ii in result:
                countryofcustomer.append(ii[0])
        for i in customerslist:
            g[i+' vector']=[0]*len(cat)
            g[i+' category-wise purchase vector']=[0]*len(cat)
            g[i+' bucket_vector']=[0]*4


            x='match(c1:customerid{CustomerID: "'+i+'"})-[r1:Bought_this]->(s1:stockcode) ' \
              'set r1.Quantity=toInteger(r1.Quantity),r1.Price=toFloat(r1.Price)' \
              'return c1.CustomerID as CustomerID, s1.Category as Category,reduce(sum=0, i in collect(r1.Quantity * r1.Price) | sum + i) as totalspent , reduce(sum=0, i in collect(r1.Quantity) | sum + i) as Quantity ' \
              'order by totalspent desc ' \

            result=session.run(x)
            count=0
            for i in result:
                count=count+1
                if count==1:

                    totalspent.append(i['totalspent'])
                    category.append(i['Category'])
                    #print(i['totalspent'])
                    if i['Category'] in cat:
                        vv = cat.index(i['Category'])
                        g[i['CustomerID'] + ' category-wise purchase vector'][vv]=i['Quantity']

                else:
                    if i['Category'] in cat:
                        vv = cat.index(i['Category'])
                        g[i['CustomerID'] + ' category-wise purchase vector'][vv]=i['Quantity']

        for i in range(0,len(customerslist)):
            x='match(c1:customerid{CustomerID:"'+customerslist[i]+'"})-[r1:Bought_this]->(s1:stockcode{Category:"'+category[i]+'"}) ' \
              'set r1.Quantity=toInteger(r1.Quantity),r1.Price=toFloat(r1.Price) ' \
              'return c1.CustomerID as CustomerID,collect(r1.Actual_Price) as prices_in_category'
            result=session.run(x)

            for yy in result:
                # print(yy[1])
                most_buyed_item_cost.append(float(Most_Common(yy[1])))

        for i in customerslist:
            dd='match(c1:customerid{CustomerID: "'+i+'"})-[r1:Bought_this]->(s1:stockcode) set r1.Quantity=toInteger(r1.Quantity),r1.Price=toFloat(r1.Price) return c1.CustomerID as CustomerID, collect( distinct s1.Category) as Categoryss'
            result=session.run(dd)
            for uu in result:
                for hh in uu['Categoryss']:
                    #print(hh)

                    if hh in cat:
                        vv = cat.index(hh)
                        g[i + ' vector'][vv]=1

        for t in range(0,len(customerslist)):

            if category[t] in cat:
                vv=cat.index(category[t])
            l = drop_in_bucket(starts[vv], ends[vv], bucketsizes[vv], most_buyed_item_cost[t])
            pricesensi.append(l)
        ageassign(pricesensi)
        df = pd.DataFrame(columns=['age', 'p_s', 'category', 'totalspent','total_cat_bought', 'country'])
        for t in range(0, len(customerslist)):
            #print(t)
            if category[t] in cat:
                vv = cat.index(category[t])
            # print('------------------------------------------------------------------------------------------------------------------')
            # print('customer                                         :',customerslist[t])
            # print('customer age                                     :',ages[t])
            # print('country                                          :',countryofcustomer[t])
            # print('total spent                                      :',totalspent[t])
            # print('category spent                                   :',category[t])
            # print('customer category vector                         :',g[customerslist[t]+' vector'])
            if pricesensi[t]=='High':
                g[customerslist[t] + ' bucket_vector'][0] = 1
            if pricesensi[t]=='Medium High':
                g[customerslist[t] + ' bucket_vector'][1] = 1
            if pricesensi[t]=='Medium Low':
                g[customerslist[t] + ' bucket_vector'][2] = 1
            if pricesensi[t]=='Low':
                g[customerslist[t] + ' bucket_vector'][3] = 1
            # print('customer category-wise purchase vector           :', g[customerslist[t] + ' category-wise purchase vector'])
            # print('customer bucket vector                           :',g[customerslist[t] +' bucket_vector'])
            # print('starting price of that category                  :',starts[vv])
            # print('ending price of that category                    :',ends[vv])
            # print('bucket size of category                          :',bucketsizes[vv])
            # print('most buyed item cost                             :',most_buyed_item_cost[t])
            # print('price sensitivity                                :',pricesensi[t])
            # print('total catogories bought                          :',sum(g[customerslist[t]+' vector']))
            # print('Yes/No                                           :',target[t])
            df=df.append({'age':ages[t],'p_s':pricesensi[t],'category':category[t],'totalspent':totalspent[t],'total_cat_bought':int(sum(g[customerslist[t] + ' vector'])),'country':countryofcustomer[t]},ignore_index=True)


        # print(df)
        df=df.drop('country',axis=1)


        hot_ps = pd.get_dummies(df.p_s)
        df = df.join(hot_ps)
        df = df.drop('p_s', axis=1)

        hot_category=pd.get_dummies(df.category)
        df = df.join(hot_category)
        df = df.drop('category', axis=1)

        # hot_country = pd.get_dummies(df.country)
        # df=df.join(hot_country)
        # df=df.drop('country',axis=1)

        data = df.values
        train_target = target
        train_data = data
        # print(train_target)
        x = tree.DecisionTreeClassifier()
        print("##################____________________productname",productname)
        print(train_data)
        print(train_target)
        x.fit(train_data, train_target)
        dot_data = StringIO()
        tree.export_graphviz(x, out_file=dot_data, feature_names=df.columns.tolist(), class_names=['No','Yes'], filled=True, rounded=True, impurity=False)
        # tree.export_graphviz(x,out_file='tree.dot')
        for i in dot_data:
            print(i)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        # print(graph)
        #os.remove("D:\E-commerce_data_visualization\search\static\stuff/segment.png") 
        # os.remove(file) for file in os.listdir('path/to/directory') if file.endswith('.png')
        # os.system(rm ,"D:\E-commerce_data_visualization\search\static\stuff/segment.png")
        graph.write_png(os.path.join(base_dir , 'search/static/stuff/segment.png'))
        print(productname,"productname727")
    # ###########################################write the above values to database#####################################
    if productname is not None:
        print(customerid)
        if customerid is None:
            customer_segment(customerslist,productname)
        else:
            print('error page with segmentation cannot be done with productname and customerid')
            exit()
    elif productname is None:
        if customerid is not None:
            product_segment(productslist, customerid)
        else:
            print('error page with segmentation cannot be done with productname and customerid1')
            exit()

##-------------------------------------           Query and nlp part    -------------------------------------------------------##

def query_and_nlp(function_call,text):
    print(text)
    from nltk.stem import PorterStemmer
    replacedlistwithnodot = []
    replacedlist = []
    replacedlist1=[]
    pos=[]
    errorno = 0
    replacedlistwithnos = []
    list = []
    x=''
    global session
    stopwords1 = set(stopwords.words('english'))
    # Change the path according to your system
    st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
    

    def spellcheck(word):
        def words(text): return re.findall(r'\w+', text)
        WORDS = Counter(words(open(os.path.join(base_dir , 'search/big.txt')).read()))
        def P(word, N=sum(WORDS.values())):
            "Probability of `word`."
            return WORDS[word] / N
        def correction(word):
            "Most probable spelling correction for word."
            return max(candidates(word), key=P)
        def candidates(word):
            "Generate possible spelling corrections for word."
            return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
        def known(words):
            "The subset of `words` that appear in the dictionary of WORDS."
            return set(w for w in words if w in WORDS)
        def edits1(word):
            "All edits that are one edit away from `word`."
            letters = 'abcdefghijklmnopqrstuvwxyz'
            splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
            deletes = [L + R[1:] for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
            replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts = [L + c + R for L, R in splits for c in letters]
            return set(deletes + transposes + replaces + inserts)
        def edits2(word):
            "All edits that are two edits away from `word`."
            return (e2 for e1 in edits1(word) for e2 in edits1(e1))
        return correction(word)

    ##########################################################################################################################
    where1 ='where '
    custo=re.findall(r"\D(\d{5})", text) 
    year1 = re.findall(r"\D(\d{4})", text) or re.findall(r"\D(\d{4})\D", text)
    if len(year1) == 0:
        where1 = where1
    elif len(year1) > 1:
        if 'top' in text.lower():
            print("try year after year")
            exit()
        if int(year1[0]) > 2016 or int(year1[0]) < 2010:
            print('sorry i dont have that information')
            exit()


    elif len(year1) == 1 and 'top' in text.lower():
        year = year1[0]
        where1 = where1 + 'r.Year=' + "'" + year + "'"
    print('year',year1)
    ##################################################YEAR COMPLETED########################################
    tokenized_text=[]
    tokenized_tex = word_tokenize(text)
    for i in tokenized_tex:
        tokenized_text.append(spellcheck(i))
    didyoumean=''
    didyoumean=' '.join(map(str, tokenized_text))
    print(didyoumean*3)
    ##########################################CORRECTION COMPLETED############################################################
    global productname
    productname=hasproductname.hasProductName(''+didyoumean)
    global customerid
    if len(custo)>0:
        customerid=hasproductname.hascustomerid(custo[0])
    else:
        customerid=None
    ############################################YEAR COMPLETED################################################################
    for i in tokenized_text:
        if i not in stopwords1:
            list.append(i.lower())
            pos.append(i)
    classified_text = st.tag(pos)
    print('classified_text',classified_text)
    count=0
    index=0
    locationsfound = 0
    for i in classified_text:
        count = count+1
        if i[1] =='LOCATION':
            index=count
            locationsfound = locationsfound+1
    print(index)
    print(locationsfound)
    print(list)
    print("productname",productname)
    if locationsfound == 0:
        where1 =where1
    elif locationsfound == 1:
        if classified_text[index-1][0] in ['United Kingdom', 'EIRE', 'Germany', 'France', 'Belgium',
         'Portugal', 'Finland', 'Spain', 'Austria','Iceland', 'Cyprus', 'Norway', 'Japan', 'Switzerland',
          'Canada', 'Sweden', 'Malta', 'Netherlands','Czech Republic', 'Lithuania', 'Australia', 'Italy',
           'Denmark', 'European Community', 'Israel','Singapore', 'Channel Islands', 'Greece', 'RSA', 'USA',
            'Bahrain', 'Brazil', 'Poland', 'Lebanon','United Arab Emirates', 'Saudi Arabia']:
            if where1=='where ':
                where1 = where1+"r.Country=" + "'"+ classified_text[index-1][0] +"'"
                print(where1)
            else:
                where1=where1+" and r.Country=" + "'"+ classified_text[index-1][0] +"'"
        else:
            print('we dont have that info')
            exit()
    elif locationsfound>1:
        print('please first search for one Location')
        exit()
     ############################################LOCATION COMPLETE#############################################################

    A=['Product','Location','Customer']
    B=['Quantity','Revenue']
    C=['Price']
    print('list',list)
    for i in list:

            replace =MyDictionary.dictionary(i)
            replacedlist1.append(replace)

    print('replacedlist1',replacedlist1)

    for i in replacedlist1:
        if i is not None:
            replacedlist.append(i)
    print('replacedlist',replacedlist)
    for ii in replacedlist:
        replacedlistwithnodot.append(ii.split('.')[1])
        replacedlistwithnos.append(ii.split('.')[1])
    if 'Description' in replacedlistwithnodot:
        replacedlistwithnos.remove("Description")
    ####selecting functions goes here############################

    if function_call=="top" or function_call=="bottom":
        col_length=top_bottom(replacedlist,replacedlistwithnodot,replacedlistwithnos,where1,function_call)

    elif function_call=='trend':
        col_length=trend(replacedlist,replacedlistwithnodot,replacedlistwithnos,productname,year1,where1)



    elif function_call=='segment':
        col_length=2
        x='match(c:customerid)-[r:Bought_this]->(s:stockcode)'\
        'return s.Description as description,collect(DISTINCT r.Price) as price '\
        'order by description'
        result = session.run(x)

        for i in result:

                    xxy = 'match p=(c:customerid)-[r:Bought_this]->(s:stockcode{Description:"'+ i['description']+'"}) set r.Actual_Price="'+str(max(i['price']))+'"'
                    session.run(xxy)

        ###########################################################################################################################################################

        x='match p=(c:customerid) with collect(distinct c.CustomerID) as customerspresent return customerspresent'
        y='match p=(c:stockcode) with collect(distinct c.StockCode) as productspresent return productspresent'
        result = session.run(x)
        result1 = session.run(y)
        for i in result:
            for ii in i[0]:
                customerslist.append(ii)
        for i in result1:
            for ii in i[0]:
                productslist.append(ii)
        # print('customerslist',customerslist)
        print(customerid,"customerid") 
        segemnt(productname,productslist,customerid,customerslist)
    return col_length

    #----------------run neo4j database  for queries  and write in csv format---------------------------------#

#----------------------------Web app connectivity---------------------------------------#
def error_page(request):
    return render(request,'error_page.html')

def sample(request):
    return render(request,'sample_queries.html')
#----------------------------graph plot section------------------------------------------#
def graph_bar_3(request):
    return render(request,'graph_bar_3.html')

def graph_bar_2(request):
    return render(request,'graph_bar_2.html')

def dicision_tree(request):
    return render(request,'dicision_tree.html')

def trend_2(request):
    return render(request,'trend_2.html',{"productname":productname})

def trend_3(request):
    return render(request,'trend_3.html')

def segment(request):
    return render(request,'segment.html')