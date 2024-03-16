from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import os 
from deeplearning import OCR

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)




@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('Index.html', students=data)


@app.route('/insert', methods = ['POST','GET'])
def insert():
    if request.method == "POST":
        print(request.form)
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        # photo = request.form['photo']
        


        upload_file = request.form['photo']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH,filename)
        upload_file.save(path_save)
        photo = OCR(path_save,filename)

        
      

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone,photo) VALUES (%s, %s, %s,%s)", (name, email, phone,photo))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    
        

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        photo = request.form['photo']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students SET name=%s, email=%s, phone=%s,photo=%s
        WHERE id=%s
        """, (name, email, phone, photo,id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/send')
def Send():
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM students")
    data = cur.fetchall()
    # print("Email is" +data)

    emails = [row[0] for row in data]  # Extracting emails from the result

    print("Emails are:", emails) 
    cur.close()

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
