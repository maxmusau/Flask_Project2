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
    
# run theh app
app.run(debug=True)