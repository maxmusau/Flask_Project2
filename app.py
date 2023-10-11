from flask import *
import pymysql
# create the app
app=Flask(__name__)
# define the connection
connection=pymysql.connect(host="localhost",user="root",database="bookings_db",password="")
# create the main
@app.route("/")
def Main():
    return "Welcome to our application. Type the route name in the address bar"

# create the room-upload route
@app.route("/upload_room",methods=['GET','POST'])
def Upload_room():
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
    


# run theh app
app.run(debug=True)