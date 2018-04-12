#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on 15. ozu 2018.

@author: Katarina123
'''

from flask import Flask, render_template, json, request, redirect, url_for, Response
from flask_mysqldb import MySQL


allDataFromDB = []
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'personpublicinfo'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


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


@app.route('/showPolitics', methods=['GET', 'POST'])
def showPolitics():
    if request.method == "POST":
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


        search = request.form['showPolitics']

        cursor.execute(stmnt1, (search,"Politika"))
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            return render_template('politika.html', records=records) 
        else:
            cursor.execute(stmnt2, (search,"Politika"))
            conn.commit()
            records = cursor.fetchall()
            if(records):
                return render_template('politika.html', records=records)
            else:
                bothNameSurname = search.split(" ")
                print (bothNameSurname)
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Politika"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('politika.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Politika"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('politika.html', records=records)
    return render_template('politika.html')



@app.route('/showMusic', methods=['GET', 'POST'])
def showMusic():
    if request.method == "POST":
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


        search = request.form['showMusic']

        cursor.execute(stmnt1, (search,"Glazba"))
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            return render_template('glazba.html', records=records) 
        else:
            cursor.execute(stmnt2, (search,"Glazba"))
            conn.commit()
            records = cursor.fetchall()
            if(records):
                return render_template('glazba.html', records=records)
            else:
                bothNameSurname = search.split(" ")
                print (bothNameSurname)
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Glazba"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('glazba.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Glazba"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('glazba.html', records=records)
    return render_template('glazba.html')



@app.route('/showSport', methods=['GET', 'POST'])
def showSport():
    if request.method == "POST":
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



        search = request.form['showSport']
        all_searches = (search, "Sport")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if (records):
            return render_template('sport.html', records=records) 
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                return render_template('sport.html', records=records)
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Sport"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('sport.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Sport"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('sport.html', records=records)
    return render_template('sport.html')



@app.route('/showTheatre', methods=['GET', 'POST'])
def showTheatre():
    if request.method == "POST":
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



        search = request.form['showTheatre']
        all_searches = (search,"Kazalište")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            return render_template('kazaliste.html', records=records) 
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                return render_template('kazaliste.html', records=records)
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "Kazalište"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('kazaliste.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "Kazalište"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('kazaliste.html', records=records)
    return render_template('kazaliste.html')


@app.route('/showTV', methods=['GET', 'POST'])
def showTV():
    if request.method == "POST":
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



        search = request.form['showTV']
        all_searches = (search,"TV")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        if(records):
            return render_template('tv.html', records=records) 
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                return render_template('tv.html', records=records)
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) == 2):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1]), "TV"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('tv.html', records=records)
                elif(len(bothNameSurname) == 3):
                    cursor.execute(stmnt3, (bothNameSurname[0], str(bothNameSurname[1] + " " + bothNameSurname[2]), "TV"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('tv.html', records=records)
    return render_template('tv.html')

if __name__ == "__main__":
    app.run()