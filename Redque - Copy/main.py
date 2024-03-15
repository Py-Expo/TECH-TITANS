from flask import Flask,request, render_template,redirect,url_for,flash
from flask_mysqldb import MySQL


app=Flask(__name__)

app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_DB']= "redque"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "6385623012"
app.config['MYSQL_CURSORCLASS']="DictCursor"
app.secret_key="myapp"
conn = MySQL(app)




def pat(Name,Email,Contact,DOB,Gender,Date,Timeslot,Reason):
    try:
        con=conn.connection.cursor()
        sql = "INSERT INTO patients(Name,Email,Contact,DOB,Gender,Date,Timeslot,Reason) values(%s,%s,%d,%s,%s,%s,%s,%s)"
        result=con.execute(sql,(Name,Email,Contact,DOB,Gender,Date,Timeslot,Reason))
        con.commit()
        return True
    except Exception as e:
        print("Error")
        return False
    finally:
        if con.is_connected():
            con.close()

@app.route('/',methods = ['POST','GET'])
def home():
    if request.method  == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Contact = request.form['Contact']
        DOB = request.form['DOB']
        Date = request.form['Date']
        Gender = request.form['Gender']
        Timeslot = request.form['Timeslot']
        Reason = request.form['Reason']
        if pat(Name,Email,Contact,DOB,Gender,Date,Timeslot,Reason):
            return redirect(url_for('home'))
    return render_template("home.html")

@app.route('/welcome', methods = ['POST', 'GET'])
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method  == 'POST':
        user_name1 = request.form['user_name']
        password1 = request.form['password']
        cod = request.form['Code']
        con=conn.connection.cursor()
        sql = "select Username, Password, Code from dsignup WHERE Username= %s and  Password=%s and Code = %s"
        result = con.execute(sql, (user_name1, password1, cod))
        if result:
            con.connection.commit()
            con.close()
            return redirect(url_for('welcome'))
        else:
            return "Invalid Username or Password"
    return render_template("login.html") 

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method  == 'POST':
        mailid = request.form['Email']
        user_name1 = request.form['Username']
        password1 = request.form['Password']
        cod = request.form['Code']
        con=conn.connection.cursor()
        sql = "INSERT INTO dsignup values(%s,%s,%s,%s)"
        result=con.execute(sql,(mailid,user_name1,password1,cod))
        con.close()
        return redirect(url_for('login'))
    return render_template("signup.html") 



@app.route('/doctor', methods = ['POST', 'GET'])
def doctor():
    return render_template("doctor.html")


if __name__ == "__main__":
    app.run(debug=True)