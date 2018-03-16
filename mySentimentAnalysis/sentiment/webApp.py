'''
Created on 15. ozu 2018.

@author: Katarina123
'''

from flask import Flask, render_template, json, request

from flask_mysqldb import MySQL



app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'personpublicinfo'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def hello():
    conn = mysql.connection
    cursor = conn.cursor()
    #cursor.execute('''SELECT * from person''')
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob
            )
    VALUES (%s,%s,%s)"""#, ("Kolinda", "Grabar-Kitarovic", "Predsjednica"))
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob
            )
    VALUES (%s,%s,%s)"""#, ("Andrej", "Plenkovic", "Premijer"))
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob
            )
    VALUES (%s,%s,%s)"""#, ("Kolinda", "Grabar-Kitarovic", "Predsjednica"))
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob
            )
    VALUES (%s,%s,%s)"""#, ("Zeljko", "Bebek", "Pjevac"))
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob
            )
    VALUES (%s,%s,%s)"""#, ("Tarik", "Filipovic", "Glumac"))
    
    #conn.commit()
    
    #cursor.execute(
    """INSERT INTO 
        person (
            personName,
            personSurname,
            personJob
            )
    VALUES (%s,%s,%s)"""#, ("Domagoj", "Duvnjak", "Rukometas"))
    
    #conn.commit()
    
    sqlQ = "SELECT * FROM person"
    cursor.execute(sqlQ)
    result_set = cursor.fetchall()
    #print (result_set)
    for row in result_set:
        print (row[0], row[1], row[2])   
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run()