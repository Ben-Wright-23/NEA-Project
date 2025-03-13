from flask import Blueprint,render_template,session


dashboardBlueprint = Blueprint("dashboard",__name__)
#create a flask blueprint for the function to load the dashboard

@dashboardBlueprint.route("/dashboard")
#routes the dashboardBlueprint with /dashboard so other areas of the program can access the blueprint
def dashboard():
    #defines the function
    session["accountDeletionError"] = ""
    #clears the error with account deletion when leaving that page so it doesn't reappear when the delete account page is reloaded
    session["tournamentCreationError"] = ""
    # clears the error with tournament creation when leaving loading the dashboard so it doesn't reappear when the tournament creation page is reloaded
    return render_template("dashboard.html", error = session["viewCodeInputError"])
    #loads the dashboard.html page 
    #passes in the session for view code input errors so they can be displayed if a invalid view code is entered
    
