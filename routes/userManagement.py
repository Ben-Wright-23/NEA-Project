from flask import Blueprint, render_template, request, redirect,session
from database import DatabaseHandler

### Blueprints ###
signupBlueprint = Blueprint("signup",__name__)
#create a flask blueprint for the function to load the signup page
createUserBlueprint = Blueprint("createUser",__name__)
#create a flask blueprint for the function to handle the link between the interface and database and the displaying of errors with the signup
authenticateUserBlueprint = Blueprint("authenticateUser",__name__)
#create a flask blueprint for the function to check the entered details are in the database and to handle redirecting the user depending on the result
deleteAccountBlueprint = Blueprint("deleteAccount",__name__)
#create a flask blueprint for the function to load the account deletion confirmation page
deleteUserBlueprint = Blueprint("deleteUser",__name__)
#create a flask blueprint for the function to handle deleting the user depending on what they enter in the username confirmation
logoutBlueprint = Blueprint("logout",__name__)
#create a flask blueprint for the function to log the user out 

### Routes ###
@signupBlueprint.route("/signup")
#creates the route for the signup blueprint, allowing it to be accessed easily
def signup():
    errorMessage = session.get("errorMessage") if session.get("errorMessage") else ""
    #if there is an error message from a prevous signup attempt, this is added to the signup page
    return render_template("Signup.html", error=errorMessage)
    #function loads the signup.html page, with the error message displayed when it is reloaded

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

    response = db.createUser(username,password)
    #calls the database function to attempt to add the user with the entered details into the database
    if response==True:
        #if data added to database successfully
        session["errorMessage"] = ""
        #There is no error message
        return redirect("/")
        #redirect to login page
    elif password != repassword:
        session["errorMessage"] = "Passwords do not match"
        #if passwords do not match, this becomes the error message
        return redirect("/signup")
        #reloads signup page, with this error message displayed (done in the html)
    elif len(username) >=16:
        session["errorMessage"] = "Username too long, must be less than 16 Characters."
        #if the username is too long, this becomes the error message
        return redirect("/signup")
        #reloads signup page, with this error message displayed (done in the html)
    elif len(username) <= 3:
        session["errorMessage"] = "Username too short, must be more than 3 Characters. "
        #if the username is too short, this becomes the error message
        return redirect("/signup")
        #reloads signup page, with this error message displayed (done in the html)
    elif len(password) <= 7:
        session["errorMessage"] = "Password too short, must be more than 6 Characters. "
        #if the password is too short, this becomes the error message
        return redirect("/signup")
        #reloads signup page, with this error message displayed (done in the html)
    elif any(char.isdigit() for char in password) == False:
        session["errorMessage"] = "Password must include number"
        #if the password does not contain a number, this becomes the error message
        return redirect("/signup")
        #reloads signup page, with this error message displayed (done in the html)
    else:
        session["errorMessage"] = "This username is taken"
        #if none of these errors have occured, the only possible issue is that the username is already taken, so this becomes the error message
        return redirect("/signup")
        #reloads signup page, with this error message displayed (done in the html)

@authenticateUserBlueprint.route("/authenticate", methods = ["post"])
#creates the route for the authenticateUser blueprint, allowing it to be directed to easily. Post method as it allows data to be sent to the server side which is required as the user is entering data. 
def authenticateUser():
    #defines function
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database and where the entities will be stored
    username = request.form["username"]
    #takes the entered username part of the data sent from the login page(the client) to the server, using the form input with id "username".
    password = request.form["password"]
    #takes the entered password part of the data sent from the login page(the client) to the server, using the form input with id "password".

    if db.authenticateUser(username, password) == True:
        #if an account is found that mathes the details the user has entered
        session["currentUser"] = username
        #creates a session for the current user, using their username for this as it is unique to their account
        return redirect("/dashboard")
        #redirects the user to their dashboard within their account
    else:
        return redirect("/")
        #otherwise reload the login page if an account with matching details was not found


@deleteAccountBlueprint.route("/deleteAccount")
#creates route for the deleteAccount blueprint, so it can be redirected to easily.
def deleteAccount():
    #defines function
    accountDeletionError = session.get("accountDeletionError") if session.get("accountDeletionError") else ""
    #If the accountDeletionError session contains something, this becomes the accountDeletionError, otherwise the accountDeletionError is blank
    return render_template("deleteAccount.html", error = accountDeletionError)
    #loads the deleteAccount.html page, with the error being sent with it being the accountDeletionError



@deleteUserBlueprint.route("/deleteUser", methods = ["post"])
#creates route for the deleteUser blueprint, so it can be accessed by other parts of the program easily. 
#Post method as handling requests from client to server
def deleteUser():
    #defines function
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database and where the entities will be stored
    username = request.form["username"]
    #takes the entered username part of the data sent from the delete account page(the client) to the server, using the form input with id "username".
    if username == session["currentUser"]:
        #if the username entered by the user is the same as the current user's username
        session["accountDeletionError"] = ""
        #there is no error with the account deletion so the error is set to nothing
        db.deleteUser(session["currentUser"])
        #call the database function to remove the account with the current user's username
        return redirect("/")
        #redirect the user to the login page
    else:
        #if the entered username does not match the current user's username
        session["accountDeletionError"] = "This is not your username"
        #there is an error with the account deletion so the error is set to a suitable message
        return redirect("/deleteAccount")
        #reload the delete account page

@logoutBlueprint.route("/logout")
#creates route for the logout blueprint, so it can be accessed by other parts of the program easily
def logout():
    #defines function
    session.clear()
    #clears all sessions, removing any data being help about the current user
    return redirect("/")
    #redirects the user to the login page