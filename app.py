from flask import *
import pymysql
# create the app
app=Flask(__name__)
# define the secret key
app.secret_key='jjgdjgaj$%#&@^LJKGDSFD'
# define the connection
connection=pymysql.connect(host="localhost",user="root",database="bookings_db",password="")
# create the main

@app.route("/")
def Main():
    return render_template("index.html")

# create the room-upload route
@app.route("/upload_room",methods=['GET','POST'])
def Upload_room():
    if 'key_admin' not in session:
        return redirect("/admin")
    # check if user has posted anything
    if request.method == 'POST':
        # TODO
         # get the records from the user/form
        room_name=request.form['room_name']
        room_desc=request.form['room_desc']
        cost=request.form['cost']
        availability=request.form['availability']
        square_feet=request.form['square_feet']
        image=request.files['image_url']
        # check if user has filled in all the records
        if not room_name or not room_desc or not cost or not availability or not square_feet or not image:
            return render_template("upload_room.html",error="Please fill all the records")
        # save the image inside the static folder
        image.save('static/images/'+image.filename)
        # pick the name of the image
        image_url=image.filename
        # create cursor-to execute the sql query
        cursor=connection.cursor()
        # define the sql query
        sql='insert into rooms(room_name,room_desc,cost,availability,square_feet,image_url) values(%s,%s,%s,%s,%s,%s)'
        values=(room_name,room_desc,cost,availability,square_feet,image_url)
        # execute the sql query
        cursor.execute(sql,values)
        connection.commit()
        return render_template("upload_room.html",message="Room uploaded successfully")
    else:  
        return render_template("upload_room.html")


# CRUD operation
# C- create-save records-POST
# R-read- select, retrieve,view-GET
# U- update-edit-PUT
# D-delete-remove-DELETE
@app.route("/getrooms", methods=['GET','POST'])
def Get_rooms():
    # define the connection
    sql='select * from rooms'
    # cursor function-to execute the sql
    cursor=connection.cursor()
    # execute the sql query
    cursor.execute(sql)
    # fetch the records
    records=cursor.fetchall()
    # check if there's records saved in the database
    if cursor.rowcount ==0:
        return render_template("rooms.html",error="No rooms available")
    else:
        print(records)  
        return render_template("rooms.html",rooms=records)
        # return jsonify(records)
    
        
# create a table called users
# columns = username, email, phone, pasword, confirm password
# 
# signup route
@app.route("/signup",methods=['GET','POST'])
def Signup():
    if request.method =='POST':
        # TODO
         # get the data from the form
         username=request.form['username']
         email=request.form['email']
         phone=request.form['phone']
         password=request.form['password']
         confirm_password=request.form['confirm_password']
        #  connection  already defined
        # input validation
         if not username or not email or not phone or not password or not confirm_password:
            return render_template("signup.html",error="Please fill in all the records")
         if password != confirm_password:
             return render_template("signup.html",error="Password do not match confirm password")
         elif " " in username:
             return render_template("signup.html",error="Username must be one word")
         elif '@' not in email:
             return render_template("signup.html",error="Email must have @")
         elif len(password) <4:
             return render_template("signup.html",error="Password must have 4 digits")
         else:
            #  check if the user exists
             sql_check_user='select * from users where username=%s'
             cursor_check_user=connection.cursor()
             cursor_check_user.execute(sql_check_user, username)
             if cursor_check_user.rowcount==1:
                 return render_template("signup.html",error="Username already exists")
             
             sql_save='insert into users (username,email,phone,password) values(%s,%s,%s,%s)'
             values=(username,email,phone,password)
            #  curcor functio
             cursor_save=connection.cursor()
            #  execute the sql query
             cursor_save.execute(sql_save,values)
            # commit
             connection.commit()
             return render_template("signup.html",message="Signup Successful")
    else:
        return render_template("signup.html")
# signin
@app.route("/login",methods=['GET','POST'])
def Signin():
    # check the method
    if request.method=='POST':
        # TODO
        username=request.form['username']
        password=request.form['password']
        # define the sql query
        sql='select * from users where username=%s and password=%s'
        # create cursor functon
        cursor=connection.cursor()
        # execute the sql
        cursor.execute(sql,(username,password))
        # check if user exists
        if cursor.rowcount==0:
            return render_template("signup.html",error="Incorrect login credentials. Try again")
        # create the user sessions
        session['key']=username
        # fetch the other columns
        user=cursor.fetchone()
        session['email']=user[1]
        session['phone']=user[2]
        return redirect("/getrooms")   
    else:
        return render_template("signup.html")
# clear the session
@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/login")

@app.route("/logout_admin")
def Logout_admin():
    session.clear()
    return redirect("/admin")

# login route for admin
@app.route("/admin",methods=['GET','POST'])
def Admin():
    # check the method
    if request.method=='POST':
        # TODO
        username=request.form['username']
        password=request.form['password']
        # define the sql query
        sql='select * from users where username=%s and password=%s'
        # create cursor functon
        cursor=connection.cursor()
        # execute the sql
        cursor.execute(sql,(username,password))
        # check if user exists
        if cursor.rowcount==0:
            return render_template("admin.html",error="Incorrect login credentials. Try again")
        admin=cursor.fetchone()
        role=admin[0]
        if role != 'admin':
            return render_template("admin.html",error="Incorrect login credentials. Try again")
        # create the user sessions
        session['key_admin']=username
        # fetch the other columns
        # user=cursor.fetchone()
        # print(user)
        session['email_admin']=admin[1]
        session['phone_admin']=admin[2]
        return redirect("/upload_room")   
    else:
        return render_template("admin.html")

# single item route
@app.route("/single_room/<room_id>",methods=['GET','POST'])
def Single_item(room_id):
    # check if user has signed in/session is live
    if 'key' not in session:
        return redirect("/login")
    else:
        # define thee sql query
        sql='select * from rooms where room_id=%s'
        # create the cursor function 
        cursor=connection.cursor()
        # execute the sql query
        cursor.execute(sql,room_id)
        # check if product exists
        if cursor.rowcount==0:
            return render_template("single_item.html",error="Prodcut does not exist")
        # fetch the product info
        room=cursor.fetchone()
        # return the variable room
        # return jsonify(room)
        return render_template("single_item.html",data=room)
    

# mpesa integration route
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
@app.route("/mpesa_payment",methods=['POST','GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "u5fdN03MHa698AzeW3rZWzMFlwkPFHGj"
        consumer_secret = "vaoNoGPXaS4qelsP"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379" #test paybil
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount":amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href='' class="btn btn-dark btn-sm">Back to Products</a>'
    else:
        return render_template("single_html.html")
    


# run theh app
app.run(debug=True)