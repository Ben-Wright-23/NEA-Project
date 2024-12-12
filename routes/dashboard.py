from flask import Blueprint,render_template


dashboardBlueprint = Blueprint("dashboard",__name__)
#create a flask blueprint for the function to load the dashboard

@dashboardBlueprint.route("/dashboard")
#routes the dashboardBlueprint with /dashboard so other areas of the program can access the blueprint
def dashboard():
    #defines the function
    return render_template("dashboard.html")
    #loads the dashboard.html page 
