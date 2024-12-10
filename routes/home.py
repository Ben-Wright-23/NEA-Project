from flask import Blueprint,render_template,session

homeBlueprint = Blueprint("home",__name__)
#create a flask blueprint for the function to load the login page

@homeBlueprint.route("/")
#route the login page with "/" which will make it the page that loads up first
def home():
    #defines function to be store in the homeBlueprint
    session["errorMessage"] = ""
    #when this page is loaded, the error pop up on the signup page should be removed so if the user goes back to the signup page, 
    #there is no error message still present from their last signup attempt
    return render_template("index.html")
    #loads the login page

    