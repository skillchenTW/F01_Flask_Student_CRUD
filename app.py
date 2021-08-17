from flask import Flask, render_template, request,flash,url_for,redirect
import psycopg2 
import psycopg2.extras
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = "skillchen_secret_key"

conn = psycopg2.connect(dbname="sampledb",user="postgres",password="dba",host="localhost",port="5433")

@app.route("/")
def Index():   
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    cur.execute("select * from students order by id")
    studentlist = cur.fetchall()
    return render_template("index.html",studentlist=studentlist)

@app.route("/add_student", methods=["POST"])    
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        cur.execute("INSERT INTO students(fname,lname,email) values(%s,%s,%s)",(fname,lname,email))
        conn.commit()
        flash("Student Added Successfully")
        return redirect(url_for("Index"))

@app.route("/edit/<id>",methods=["POST","GET"])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from students where id=%s",(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])

@app.route("/update/<id>",methods=["POST"])
def update_student(id):    
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
        update students set fname =%s, lname=%s , email=%s where id = %s
        """, (fname,lname,email,id))
        flash('Student Updated Successfully!')
        conn.commit()
        return redirect(url_for("Index"))

@app.route("/delete/<string:id>",methods=["POST","GET"])
def delete_student(id):            
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("delete from students where id={0}".format(id))
    conn.commit()
    flash("Student Removed Successfully!")
    return redirect(url_for("Index"))

if __name__ == '__main__':
    app.run(debug=True)