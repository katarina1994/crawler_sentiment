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
    
    
    
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob,
            personTag
            )
    VALUES (%s,%s,%s,%s)"""#,# ("Andrej", "Plenkovic", "Premijer", "Politika"))
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob,
            personTag 
            )
    VALUES (%s,%s,%s,%s)"""#,# ("Zeljko", "Bebek", "Pjevac", "Glazba"))
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob,
            personTag
            )
    VALUES (%s,%s,%s,%s)"""#, #("Kolinda", "Grabar-Kitarovic", "Predsjednica", "Politika"))
    #conn.commit()
    
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob,
            personTag
            )
    VALUES (%s,%s,%s,%s)"""#,# ("Tarik", "Filipovic", "Glumac", "Kazaliste"))
    
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob,
            personTag
            )
    VALUES (%s,%s,%s,%s)"""#,# ("Domagoj", "Duvnjak", "Rukometas", "Sport"))
    
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
        stmnt1 = "select * from person where personName = %s and personTag = %s"
        stmnt2 = "select * from person where personSurname = %s and personTag = %s"
        stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"
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
                if(len(bothNameSurname) > 1):
                    cursor.execute(stmnt3, (bothNameSurname[0], bothNameSurname[1], "Politika"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('politika.html', records=records)
    return render_template('politika.html')



@app.route('/showMusic', methods=['GET', 'POST'])
def showMusic():
    if request.method == "POST":
        conn = mysql.connection
        cursor = conn.cursor()
        stmnt1 = "select * from person where personName = %s AND personTag = %s"
        stmnt2 = "select * from person where personSurname = %s AND personTag = %s"
        stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"

        search = request.form['showMusic']
        all_searches = (search,"Glazba")
        cursor.execute(stmnt1, all_searches)
        conn.commit()
        #for r in cursor.fetchall():
            #print (r[0],r[1],r[2])
        records = cursor.fetchall()
        print (records)
        if(records):
            return render_template('glazba.html', records=records) 
        else:
            cursor.execute(stmnt2, all_searches)
            conn.commit()
            records = cursor.fetchall()
            if(records):
                return render_template('glazba.html', records=records)
            else:
                bothNameSurname = search.split(" ")
                if(len(bothNameSurname) > 1):
                    cursor.execute(stmnt3, (bothNameSurname[0], bothNameSurname[1], "Glazba"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('glazba.html', records=records)
    return render_template('glazba.html')



@app.route('/showSport', methods=['GET', 'POST'])
def showSport():
    if request.method == "POST":
        conn = mysql.connection
        cursor = conn.cursor()
        stmnt1 = "select * from person where personName = %s AND personTag = %s"
        stmnt2 = "select * from person where personSurname = %s AND personTag = %s"
        stmnt3 = "select * from person where personName = %s and personSurname = %s and personTag = %s"

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
                if(len(bothNameSurname) > 1):
                    cursor.execute(stmnt3, (bothNameSurname[0], bothNameSurname[1], "Sport"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('sport.html', records=records)
    return render_template('sport.html')



@app.route('/showTheatre', methods=['GET', 'POST'])
def showTheatre():
    if request.method == "POST":
        conn = mysql.connection
        cursor = conn.cursor()
        stmnt1 = "select * from person where personName LIKE %s AND personTag = %s"
        stmnt2 = "select * from person where personSurname LIKE %s AND personTag = %s"
        stmnt3 = "select * from person where personName LIKE %s and personSurname LIKE %s and personTag = %s"

        search = request.form['showTheatre']
        all_searches = (search,"Kazaliste")
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
                if(len(bothNameSurname) > 1):
                    cursor.execute(stmnt3, (bothNameSurname[0], bothNameSurname[1], "Kazaliste"))
                    conn.commit()
                    records = cursor.fetchall()
                    return render_template('kazaliste.html', records=records)
    return render_template('kazaliste.html')



if __name__ == "__main__":
    app.run()