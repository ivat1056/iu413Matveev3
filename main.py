from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/Create')
def Create():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()       # Создание таблицы students                  
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sname TEXT NOT NULL,
    grname TEXT  NOT NULL,
    sex Text NOT NULL,
    day INTEGER CHECK ((day <= 31) AND (day > 0))
    )
    ''')
    connection.commit()
    connection.close()
    return render_template("Create.html", active='Create')
@app.route('/HomePage')
def HomePage():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor() 
    cursor.execute(''' SELECT * FROM Students''')
    data  = cursor.fetchall()
    connection.close()
    return render_template("HomePage.html", data =data, active='HomePage' )
@app.route('/Insert', methods=['POST', 'GET'])
def Insert():
    if request.method == 'POST':
        name = request.form['Name']
        sname = request.form['Sname']
        grname = request.form['GName']
        sex = request.form['Sex']
        day = request.form['Day']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor() 
        cursor.execute("INSERT INTO Students (name, sname, grname, sex, day ) VALUES (?,?,?,?,?)",(name, sname, grname, sex,day))
        connection.commit()
        connection.close()
    return render_template("Insert.html", active='Insert')
@app.route('/Delete', methods=['POST', 'GET'])
def Delete():
    if request.method == 'POST':
        name = request.form['Name']
        sname = request.form['Sname']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor() 
        cursor.execute("DELETE FROM Students WHERE name=? AND sname=? ", (name, sname)) 
        connection.commit()
        connection.close()
    return render_template("Delete.html", active='Delete')
@app.route('/Select', methods=['GET', 'POST'])
def Select():
    data = ""
    if request.method == 'POST':
        grname = request.form['GName']
        sort = request.form['Sort']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor() 
        if (sort == "descending"):
            cursor.execute("SELECT name, sname  FROM Students WHERE grname=? ORDER BY sname DESC", [grname])
        else:
            cursor.execute("SELECT name, sname  FROM Students WHERE grname=? ORDER BY sname ", [grname])
        data  = cursor.fetchall()
        connection.commit()
        connection.close()
    return render_template("Select.html", data =data, active='Select')
@app.route('/Select2', methods=['POST', 'GET'])
def Select2():
    data = ""
    if request.method == 'POST':
        sex = request.form['Sex']
        day = request.form['Day']
        sort = request.form['Sort']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor() 
        if (sort == "descending"):
            cursor.execute("SELECT name, sname, grname  FROM Students WHERE sex=? AND day>? ORDER BY sname DESC", [sex],[day])
        else:
            cursor.execute("SELECT name, sname, grname  FROM Students WHERE sex=? AND day>? ORDER BY sname ", (sex, day))
        data  = cursor.fetchall()
        connection.commit()
        connection.close()
    return render_template("Select2.html", data =data, active='Select2')

if __name__ == '__main__':
    app.run()