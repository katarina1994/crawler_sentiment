#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on 15. ozu 2018.

@author: Katarina123
'''

from flask import Flask, render_template, jsonify, request, Response, json
from flask_mysqldb import MySQL
import mainPackage.systemLogic as sl
from collections import OrderedDict

allDataFromDB = []
app = Flask(__name__)
mysql = MySQL()



def runWebApplication():   
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'personpublicinfo'
    app.config['MYSQL_HOST'] = 'localhost'
    mysql.init_app(app)
    #print (__name__)
    if __name__ == "mainPackage.webApp":
        app.run()




@app.route("/", methods=['GET', 'POST'])
def hello():

    conn = mysql.connection
    cursor = conn.cursor()
    
    #cursor.execute('''SELECT * from person''')

    sqlQ = "SELECT * FROM person"
    cursor.execute(sqlQ)
    result_set = cursor.fetchall()
    #print (result_set)

    for row in result_set:
        if(str(row[1] + " " + row[2]) not in allDataFromDB):
            allDataFromDB.append(row[1] + " " + row[2])
        #print (row[0], row[1], row[2])   
    
    
    # HOW TO ADD ENTRY TO MYSQL EXAMPLE
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname
            )
    VALUES (%s,%s)"""#,# ("Domagoj", "Duvnjak",))
    
    #conn.commit()

    return render_template('index.html')



@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(allDataFromDB), mimetype='application/json')





# happening without refreshing
@app.route('/startCrawlerSentiment')
def startCrawlerSentiment():
    print ("Hello crawl")
    
    fConfig = open("configurationFiles/config.txt", "w");
    numOfArticlesToCrawl = request.args.get('numofarticles', 0, type=int)
    portalName = request.args.get('portal')
    if (portalName == "24sata"):
        fConfig.write("www.24sata.hr" + "\n")
        fConfig.write("https://www.24sata.hr/.+/.*\w+-\w+-.+-\d+$" + "\n")
        fConfig.write(str(numOfArticlesToCrawl)) 
    elif (portalName == "Index"):
        fConfig.write("www.index.hr" + "\n")
        fConfig.write("https://www.index.hr/.*/clanak/\w+-\w+.*\d+.aspx$" + "\n")
        fConfig.write(str(numOfArticlesToCrawl)) 
    elif (portalName == "Jutarnji list"):
        fConfig.write("www.jutarnji.hr" + "\n")
        fConfig.write("https://www.jutarnji.hr/.+/.*\w+-\w+-.+/\d+/$" + "\n")
        fConfig.write(str(numOfArticlesToCrawl)) 
    elif (portalName == "Večernji list"):
        fConfig.write("www.vecernji.hr" + "\n")
        fConfig.write("https://www.vecernji.hr/.+/.*\w+-\w+-.+\d+$" + "\n")
        fConfig.write(str(numOfArticlesToCrawl)) 
    else:
        return jsonify(result="ERROR! Wrong value for portal name!")
    #print (numOfArticlesToCrawl)
    #print (portalName)
    fConfig.close()
    sl.runCrawl()
    sl.runAnalizeTopicSaveDB()
    print ("DONE Crawl")
    return jsonify(result="")


# happening without refreshing
@app.route('/startRoundRobinCrawlerSentiment')
def startRoundRobinCrawlerSentiment():
    print ("Hello RR crawl")
    
    fConfig = open("configurationFiles/roundRobinConfig.txt", "a+");
    numOfArticlesToCrawl = request.args.get('numofarticles', 0, type=int)
    portalName = request.args.get('portal')
    fConfig.write(str(numOfArticlesToCrawl) + "\n")
    if ("24sata" in portalName):
        fConfig.write("www.24sata.hr" + ",")
        fConfig.write("https://www.24sata.hr/.+/.*\w+-\w+-.+-\d+$" + "\n")
    if ("Index" in portalName):
        fConfig.write("www.index.hr" + ",")
        fConfig.write("https://www.index.hr/.*/clanak/\w+-\w+.*\d+.aspx$" + "\n")
    if ("Jutarnji list" in portalName):
        fConfig.write("www.jutarnji.hr" + ",")
        fConfig.write("https://www.jutarnji.hr/.+/.*\w+-\w+-.+/\d+/$" + "\n")
    if ("Večernji list" in portalName):
        fConfig.write("www.vecernji.hr" + ",")
        fConfig.write("https://www.vecernji.hr/.+/.*\w+-\w+-.+\d+$" + "\n")
        
    #print (numOfArticlesToCrawl)
    #print (portalName)
    fConfig.close()
    sl.runCrawlRoundRobin()
    sl.runAnalizeTopicSaveDB()
    fConfig = open("configurationFiles/roundRobinConfig.txt", "r+");
    fConfig.truncate()
    fConfig.close()
    print ("DONE RR Crawl")
    return jsonify(result="")

@app.route('/startFindAll')
def startFindAll():
    print ("Hello find all")
    allPerson = sl.runFindPersonAppearanceInArticle()
    recordsPerson = []
    conn = mysql.connection
    cursor = conn.cursor()
    stmntPerson = "SELECT * from person WHERE person.id = %s"
    
    for person in allPerson:
        print (person)
        cursor.execute(stmntPerson, (person[3],))
        recordsPerson += cursor.fetchall()
    recordsPerson = list(set(recordsPerson))
    print (recordsPerson)
    print ("DONE find all")
    #records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
    #return render_template("timeline.html", records=records, recordsPerson=recordsPerson)
    return jsonify(result="")

@app.route('/startPosNegWords')
def startPosNegWords():
    print ("Hello pos neg words")
    sl.rungetsentimentAnalysisFromPosAndNegWords()
    print ("DONE pos neg words")
    return "nothing"


@app.route('/startSVM')
def startSVM():
    print ("Hello SVM")
    svm = sl.rungetsentimentAnalysisSVMModel()
    result = svm.tolist()
    conn = mysql.connection
    cursor = conn.cursor()
    index = 0
    while index < len(result):
        cursor.execute("UPDATE personinfo SET sentiment = %s WHERE id = %s", (result[index], int(index + 1)))
        conn.commit() 
        index += 1
    #print (result)
    print ("DONE SVM")
    return jsonify(result="")


@app.route('/showTimeline',  methods=['GET', 'POST'])
def startTimeline():
    print ("Hello Timeline")
    labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    recordsPerson = []
    conn = mysql.connection
    cursor = conn.cursor()
    stmntTimeline = "SELECT * from personinfo"
    stmntPerson = "SELECT * from person WHERE person.id = %s"
    cursor.execute(stmntTimeline)
    conn.commit()
    records = cursor.fetchall()
    for record in records:
        cursor.execute(stmntPerson, (record[1],))
        recordsPerson += cursor.fetchall()
    recordsPerson = list(set(recordsPerson)) 
    #print (records)
    print ("DONE Timeline")
    records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
    values,sentiment = getApperancesByMonth(records)
    listSentiment = list(sentiment)
    pos = listSentiment[0::3]
    neg = listSentiment[1::3]
    neu = listSentiment[2::3]
    return render_template('timeline.html', records=records, recordsPerson=recordsPerson, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)



@app.route('/showPolitics', methods=['GET', 'POST'])
def showPolitics():
    if request.method == "POST":
        
        labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        conn = mysql.connection
        cursor = conn.cursor()
        #stmnt1 = "select * from person where personName = %s and personTag = %s"
        #stmnt1 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and tag.tagName = %s"
        stmnt1 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and tag.tagName = %s"

        #stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        #stmnt2 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personSurname = %s and tag.tagName = %s"
        stmnt2 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personSurname = %s and tag.tagName = %s"

        #stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
        #stmnt3 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"
        stmnt3 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"

        stmnt4 = "SELECT * from personinfo WHERE personinfo.personId = %s"


        search = request.form['showPolitics']

        cursor.execute(stmnt1, (search,"Politika"))
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            personID = records[0][0]
            cursor.execute(stmnt4, (personID,))
            conn.commit()
            records = cursor.fetchall()
            records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
            values, sentiment = getApperancesByMonth(records)
            listSentiment = list(sentiment)
            pos = listSentiment[0::3]
            neg = listSentiment[1::3]
            neu = listSentiment[2::3]
            return render_template('politika.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)
        else:
            cursor.execute(stmnt2, (search,"Politika"))
            conn.commit()
            records = cursor.fetchall()
            if(records):
                personID = records[0][0]
                cursor.execute(stmnt4, (personID,))
                conn.commit()
                records = cursor.fetchall()
                #print (records)
                records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                values, sentiment = getApperancesByMonth(records)
                listSentiment = list(sentiment)
                pos = listSentiment[0::3]
                neg = listSentiment[1::3]
                neu = listSentiment[2::3]
                return render_template('politika.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
            else:
                bothNameSurname = search.split(" ")
                #print (bothNameSurname)
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Politika"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values,sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('politika.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)
                    else:
                        return render_template('politika.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Politika"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values,sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('politika.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)
                    else:
                        return render_template('politika.html', records=records)
    return render_template('politika.html')



@app.route('/showMusic', methods=['GET', 'POST'])
def showMusic():
    if request.method == "POST":
        
        labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        conn = mysql.connection
        cursor = conn.cursor()
        #stmnt1 = "select * from person where personName = %s and personTag = %s"
        #stmnt1 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and tag.tagName = %s"
        stmnt1 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and tag.tagName = %s"

        #stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        #stmnt2 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personSurname = %s and tag.tagName = %s"
        stmnt2 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personSurname = %s and tag.tagName = %s"

        #stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
        #stmnt3 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"
        stmnt3 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"

        stmnt4 = "SELECT * from personinfo WHERE personinfo.personId = %s"


        search = request.form['showMusic']

        cursor.execute(stmnt1, (search,"Glazba"))
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            personID = records[0][0]
            cursor.execute(stmnt4, (personID,))
            conn.commit()
            records = cursor.fetchall()
            records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
            values, sentiment = getApperancesByMonth(records)
            listSentiment = list(sentiment)
            pos = listSentiment[0::3]
            neg = listSentiment[1::3]
            neu = listSentiment[2::3]
            return render_template('glazba.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
        else:
            cursor.execute(stmnt2, (search,"Glazba"))
            conn.commit()
            records = cursor.fetchall()
            if(records):
                personID = records[0][0]
                cursor.execute(stmnt4, (personID,))
                conn.commit()
                records = cursor.fetchall()
                records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                values, sentiment = getApperancesByMonth(records)
                listSentiment = list(sentiment)
                pos = listSentiment[0::3]
                neg = listSentiment[1::3]
                neu = listSentiment[2::3]
                return render_template('glazba.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
            else:
                bothNameSurname = search.split(" ")
                #print (bothNameSurname)
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Glazba"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('glazba.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)  
                    else:
                        return render_template('glazba.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Glazba"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('glazba.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
                    else:
                        return render_template('glazba.html', records=records)
    return render_template('glazba.html')



@app.route('/showSport', methods=['GET', 'POST'])
def showSport():
    if request.method == "POST":
        labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        conn = mysql.connection
        cursor = conn.cursor()
        #stmnt1 = "select * from person where personName = %s and personTag = %s"
        #stmnt1 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and tag.tagName = %s"
        stmnt1 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and tag.tagName = %s"

        #stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        #stmnt2 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personSurname = %s and tag.tagName = %s"
        stmnt2 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personSurname = %s and tag.tagName = %s"

        #stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
        #stmnt3 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"
        stmnt3 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"

        stmnt4 = "SELECT * from personinfo WHERE personinfo.personId = %s"


        search = request.form['showSport']
        all_searches = (search, "Sport")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if (records):
            personID = records[0][0]
            cursor.execute(stmnt4, (personID,))
            conn.commit()
            records = cursor.fetchall()
            records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
            values, sentiment = getApperancesByMonth(records)
            listSentiment = list(sentiment)
            pos = listSentiment[0::3]
            neg = listSentiment[1::3]
            neu = listSentiment[2::3]
            return render_template('sport.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)   
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                personID = records[0][0]
                cursor.execute(stmnt4, (personID,))
                conn.commit()
                records = cursor.fetchall()
                records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                values, sentiment = getApperancesByMonth(records)
                listSentiment = list(sentiment)
                pos = listSentiment[0::3]
                neg = listSentiment[1::3]
                neu = listSentiment[2::3]
                return render_template('sport.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Sport"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('sport.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
                    else:
                        return render_template('sport.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Sport"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('sport.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu) 
                    else:
                        return render_template('sport.html', records=records)
    return render_template('sport.html')



@app.route('/showTheatre', methods=['GET', 'POST'])
def showTheatre():
    if request.method == "POST":
        labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        conn = mysql.connection
        cursor = conn.cursor()
        #stmnt1 = "select * from person where personName = %s and personTag = %s"
        #stmnt1 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and tag.tagName = %s"
        stmnt1 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and tag.tagName = %s"

        #stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        #stmnt2 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personSurname = %s and tag.tagName = %s"
        stmnt2 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personSurname = %s and tag.tagName = %s"

        #stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
        #stmnt3 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"
        stmnt3 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"

        stmnt4 = "SELECT * from personinfo WHERE personinfo.personId = %s"


        search = request.form['showTheatre']
        all_searches = (search,"Kazalište")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            personID = records[0][0]
            cursor.execute(stmnt4, (personID,))
            conn.commit()
            records = cursor.fetchall()
            records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
            values, sentiment = getApperancesByMonth(records)
            listSentiment = list(sentiment)
            pos = listSentiment[0::3]
            neg = listSentiment[1::3]
            neu = listSentiment[2::3]
            return render_template('kazaliste.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)  
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                personID = records[0][0]
                cursor.execute(stmnt4, (personID,))
                conn.commit()
                records = cursor.fetchall()
                records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                values, sentiment = getApperancesByMonth(records)
                listSentiment = list(sentiment)
                pos = listSentiment[0::3]
                neg = listSentiment[1::3]
                neu = listSentiment[2::3]
                return render_template('kazaliste.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)  
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Kazalište"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('kazaliste.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)  
                    else:
                        return render_template('kazaliste.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Kazalište"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('kazaliste.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)  
                    else:
                        return render_template('kazaliste.html', records=records)
    return render_template('kazaliste.html')


@app.route('/showTV', methods=['GET', 'POST'])
def showTV():
    if request.method == "POST":
        labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        conn = mysql.connection
        cursor = conn.cursor()
        #stmnt1 = "select * from person where personName = %s and personTag = %s"
        #stmnt1 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and tag.tagName = %s"
        stmnt1 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and tag.tagName = %s"

        #stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        #stmnt2 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personSurname = %s and tag.tagName = %s"
        stmnt2 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personSurname = %s and tag.tagName = %s"

        #stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
        #stmnt3 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"
        stmnt3 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"

        stmnt4 = "SELECT * from personinfo WHERE personinfo.personId = %s"


        search = request.form['showTV']
        all_searches = (search,"TV")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            personID = records[0][0]
            cursor.execute(stmnt4, (personID,))
            conn.commit()
            records = cursor.fetchall()
            records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
            values, sentiment = getApperancesByMonth(records)
            listSentiment = list(sentiment)
            pos = listSentiment[0::3]
            neg = listSentiment[1::3]
            neu = listSentiment[2::3]
            return render_template('tv.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                personID = records[0][0]
                cursor.execute(stmnt4, (personID,))
                conn.commit()
                records = cursor.fetchall()
                records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                values, sentiment = getApperancesByMonth(records)
                listSentiment = list(sentiment)
                pos = listSentiment[0::3]
                neg = listSentiment[1::3]
                neu = listSentiment[2::3]
                return render_template('tv.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "TV"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('tv.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)
                    else:
                        return render_template('tv.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "TV"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('tv.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
                    else:
                        return render_template('tv.html', records=records)
    return render_template('tv.html')


@app.route('/showBusiness', methods=['GET', 'POST'])
def showBusiness():
    if request.method == "POST":
        labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        conn = mysql.connection
        cursor = conn.cursor()
        #stmnt1 = "select * from person where personName = %s and personTag = %s"
        #stmnt1 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and tag.tagName = %s"
        stmnt1 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and tag.tagName = %s"

        #stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        #stmnt2 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personSurname = %s and tag.tagName = %s"
        stmnt2 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personSurname = %s and tag.tagName = %s"

        #stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
        #stmnt3 = "SELECT person.*, tag.* FROM person person, tag tag WHERE person.id = tag.personId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"
        stmnt3 = "SELECT person.*, tag.*, persontag.* FROM person person, tag tag, persontag persontag WHERE person.id = persontag.personId and tag.id = persontag.tagId and person.personName = %s and person.personSurname = %s and tag.tagName = %s"

        stmnt4 = "SELECT * from personinfo WHERE personinfo.personId = %s"


        search = request.form['showBusiness']
        all_searches = (search,"Poduzetništvo")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            personID = records[0][0]
            cursor.execute(stmnt4, (personID,))
            conn.commit()
            records = cursor.fetchall()
            records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
            values, sentiment = getApperancesByMonth(records)
            listSentiment = list(sentiment)
            pos = listSentiment[0::3]
            neg = listSentiment[1::3]
            neu = listSentiment[2::3]
            return render_template('poduzetnistvo.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                personID = records[0][0]
                cursor.execute(stmnt4, (personID,))
                conn.commit()
                records = cursor.fetchall()
                records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                values, sentiment = getApperancesByMonth(records)
                listSentiment = list(sentiment)
                pos = listSentiment[0::3]
                neg = listSentiment[1::3]
                neu = listSentiment[2::3]
                return render_template('poduzetnistvo.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Poduzetništvo"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('poduzetnistvo.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
                    else:
                        return render_template('poduzetnistvo.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Poduzetništvo"))
                    conn.commit()
                    records = cursor.fetchall()
                    if(records):
                        personID = records[0][0]
                        cursor.execute(stmnt4, (personID,))
                        conn.commit()
                        records = cursor.fetchall()
                        #print (records)
                        records = tuple(sorted(records, key=lambda item: item[3], reverse=True))
                        values, sentiment = getApperancesByMonth(records)
                        listSentiment = list(sentiment)
                        pos = listSentiment[0::3]
                        neg = listSentiment[1::3]
                        neu = listSentiment[2::3]
                        return render_template('poduzetnistvo.html', records=records, values=values, labels=labels, sentiment=sentiment, pos=pos, neg=neg, neu=neu)    
                    else:
                        return render_template('poduzetnistvo.html', records=records)
    return render_template('poduzetnistvo.html')


def getApperancesByMonth(records):

    #print (records)
    listSentiment = ["pos1","neg1","neu1","pos2","neg2","neu2","pos3","neg3","neu3","pos4","neg4","neu4","pos5","neg5","neu5","pos6","neg6","neu6","pos7","neg7","neu7","pos8","neg8","neu8","pos9","neg9","neu9","pos10","neg10","neu10","pos11","neg11","neu11","pos12","neg12","neu12",]
    listMonths = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    chartMonth = OrderedDict([(key, 0) for key in listMonths]) 
    chartSentiment = OrderedDict([(key, 0) for key in listSentiment]) 
    
    for record in records:
        if(record[3].split("-")[1] == "01"):
            chartMonth["January"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos1"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg1"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu1"] += 1
        elif(record[3].split("-")[1] == "02"):
            chartMonth["February"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos2"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg2"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu2"] += 1
        elif(record[3].split("-")[1] == "03"):
            chartMonth["March"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos3"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg3"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu3"] += 1
        elif(record[3].split("-")[1] == "04"):
            chartMonth["April"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos4"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg4"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu4"] += 1
        elif(record[3].split("-")[1] == "05"):
            chartMonth["May"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos5"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg5"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu5"] += 1
        elif(record[3].split("-")[1] == "06"):
            chartMonth["June"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos6"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg6"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu6"] += 1
        elif(record[3].split("-")[1] == "07"):
            chartMonth["July"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos7"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg7"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu7"] += 1
        elif(record[3].split("-")[1] == "08"):
            chartMonth["August"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos8"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg8"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu8"] += 1
        elif(record[3].split("-")[1] == "09"):
            chartMonth["September"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos9"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg9"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu9"] += 1
        elif(record[3].split("-")[1] == "10"):
            chartMonth["October"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos10"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg10"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu10"] += 1
        elif(record[3].split("-")[1] == "11"):
            chartMonth["November"] += 1
            if(record[5] == "pos"):
                chartSentiment["pos11"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg11"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu11"] += 1
        elif(record[3].split("-")[1] == "12"):
            chartMonth["December"] += 1 
            if(record[5] == "pos"):
                chartSentiment["pos12"] += 1
            elif(record[5] == "neg"):
                chartSentiment["neg12"] += 1
            elif(record[5] == "neu"):
                chartSentiment["neu12"] += 1
    return chartMonth, chartSentiment