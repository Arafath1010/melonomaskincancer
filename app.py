#Import necessary libraries
import sqlite3
#import pyttsx3
#global e
details = ""
#e=pyttsx3.init() #for text to speach 
#e.setProperty("rate",130)
from flask import Flask, render_template, request
#import pickle
import numpy as np
import os


#database connection
con = sqlite3.connect("user.db")
print("database connected successfully")


# for ml model loading & predicting
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model



filepath = 'melonomaskincancer.hdf5'
model = load_model(filepath)
print(model)

print("Model Loaded Successfully")

#method for predict the result
global result
def diceas_predict(diceas_image):
  test_image = load_img(diceas_image, target_size = (180, 180)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  global result
  result = model.predict(test_image) # predict diseased palnt or not
  print('@@ Raw result = ', max(result))
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      details = "Dr. PRASAD ABEYSINGHE\nLanka Hospitals\n0112 551410\n0115 430000\nCeylinco Healthcare Centre\n0112 688038"
      return "melanoma - benign Disease", 'result.html',details
       
  elif pred==1:
      details = "Dr. YASANTHA ARIYARATHNA\nDurdans Hospital\n0115 410000\nNawaloka Hospital\n0112 304444\nSri Jayewardenepura General Hospital\n0112 778610\nHemas Hospital Thalawathugod\n0117 888888"
      return "melanoma- malignant Disease", 'result.html',details

        

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/index", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
    
 
#this method for login page
@app.route("/loginpage", methods = ['GET','POST'])
def loginpage():
     return render_template('login.html')

# this method for registration page
@app.route("/registerpage", methods = ['GET','POST'])
def registerpage():
     return render_template('register.html')    

#this method for landing page
@app.route("/", methods = ['GET','POST'])
def landingpage():
     return render_template('landingpage.html')

@app.route("/diabetes", methods = ['GET','POST'])
def diabetes():
    return render_template('diabetes.html')

  

# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
       # get the file from user 
        file = request.files['image'] # get input values from form inputs using there name attribute
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        # store the image  on server
        file_path = os.path.join('static/', filename)
        file.save(file_path)
        print(file_path)

        print("@@ Predicting class......")
        pred, output_page,details = diceas_predict(diceas_image=file_path)
        #e.say(pred+"predicted and the accuracy is "+str(max(result[0])))
        #e.runAndWait()   
        return render_template(output_page,doctor=details, pred_output = pred, user_image = file_path,pred_output_ac=max(result[0]))

# method for get the user login details from the login form
@app.route("/login", methods = ['GET','POST'])
def login():
     count = 0
     if request.method == 'POST':
       # get the user name from login form 
        name = request.form.get('name') # get input values from form inputs using there name attribute
        password = request.form.get('pass')
        cursor = con.execute("select * from user where name = '"+name+"' and password='"+password+"'")
        for row in cursor:
          count = count + 1
        if count>0:
          print("login successfully")
          #e.say("login successfully")
          #e.runAndWait()
          return render_template("index.html")
        else:
          print("please register with our app !")
          #e.say("please register with our app !")
          #e.runAndWait()
          return render_template("register.html")
        print("@@ Input posted = ",name)      

# method for get the user register details from the register form
@app.route("/register", methods = ['GET','POST'])
def register():
     count = 0
     if request.method == 'POST':
       # get the user name from login form 
        name = request.form.get('username') # get input values from form inputs using there name attribute
        password = request.form.get('password')
        email = request.form.get('email')
        nic = request.form.get('nic')
        dob = request.form.get('dob')
        phonenumber = request.form.get('phonenumber')
        address = request.form.get('address')
        con.execute("insert into user values('"+name+"','"+password+"','"+email+"','"
                    +nic+"','"+dob+"','"+phonenumber+"','"+address+"')")
        con.commit()
        #e.say("hi "+name+" thank you for register with us !")
        #e.runAndWait()
        return render_template("index.html")




      
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 
    
    
