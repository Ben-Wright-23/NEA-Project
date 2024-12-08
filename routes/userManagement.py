from flask import Blueprint, render_template, request, redirect
from database import DatabaseHandler

### Blueprints ###
signupBlueprint = Blueprint("signup",__name__)
#create a flask blueprint for the function to load the signup page
createUserBlueprint = Blueprint("createUser",__name__)
#cretae a flask blueprint for the function to handle the link between the interface and database and the displaying of errors with the signup

### Routes ###
@signupBlueprint.route("/")
#creates the route for the signup blueprint, allowing it to be accessed easily
def signup():
    return render_template("Signup.html")
#function to load the signup.html page

@createUserBlueprint.route("/createUser", methods = ["post"])
#creates the route for the createUser blueprint, allowing it to be accessed easily. Post method as it allows data to be sent to the server side which is required as the user is entering data. 
def createUser():
    #defines function
    db=DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database and where the entities will be stored
    username = request.form["username"]
    #takes the entered username part of the data sent from the signup page(the client) to the server, using the form input with id "username".
    password=request.form["password"]
    #takes the entered password part of the data sent from the signup page(the client) to the server, using the form input with id "password".
    repassword=request.form["repassword"]
    #takes the entered repassword part of the data sent from the signup page(the client) to the server, using the form input with id "repassword".
    message=""
    #creates a blank string called message that will serve as the error message

    if len(username) >=16:
        message = message + "Username too long, must be less than 16 Characters. "
        #Checks the username is not too long, if it is, adds this to list of errors
    if len(username) <= 3:
        message = message + "Username too short, must be more than 3 Characters. "
        #Checks the username is not too short, if it is, adds this to list of errors
    if len(password) <= 6:
        message = message + "Password too short, must be more than 6 Characters. "
        #Checks the password is not too short, if it is, adds this to list of errors
    if any(char.isdigit() for char in password) == False:
        message = message + "Password does not contain a number. "
        #Checks the password contains a number, if it doesn't, adds this to list of errors
    if password != repassword:
        message = message + "Passwords do not match. "
        #Checks the passwords match, if they do not, adds this to list of errors

    response = db.createUser(username,password)
    #calls the database function to attempt to add the user with the entered details into the database
    if response==True: 
        return "Successs"
        #if user added successfully, redirect to login page
    else:
        return message
        #if user not added successfully return error message
        