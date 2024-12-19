from flask import Blueprint,render_template, session, request, redirect
from database import DatabaseHandler
# import database and required flask modules

creationFormBlueprint = Blueprint("creationForm",__name__)
#create a flask blueprint for the function to load the tournamentCreation page
tournamentCreationBlueprint = Blueprint("tournamentCreation",__name__)
#create a flask blueprint for the function to link the interface and database for the tournament creation and to display errors with the tournament creation

@creationFormBlueprint.route("/creationForm")
#creates the route for the creationForm blueprint, allowing it to be accessed easily
def creationForm():
    #defines function to load creationForm page
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    #produces the error with the tournament creation if there is one
    #if no error, no error is passed to the interface
    return render_template("creationForm.html", error = Error)
    #loads the creationForm.html page, with the error message displayed when it is reloaded


@tournamentCreationBlueprint.route("/tournamentCreation", methods = ["POST"])
#creates the route for the tournamentCreation blueprint, allowing it to be accessed easily. Post method allows it to make server side changes
def tournamentCreation():
    #defines function to load creationForm page
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database and where the entities will be stored
    tournamentName = request.form["tournamentName"]
    #takes the entered tournamentName part of the data sent from the creationForm page(the client) to the server, using the form input with id "tournamentName".
    numTeams = request.form["numTeams"]
    #takes the entered number of teams part of the data sent from the creationForm page(the client) to the server, using the form input with id "numTeams".

    if db.createTournament(tournamentName,session["currentUser"],numTeams)==True:
        #if the tournament is created successfully
        session["tournamentCreationError"] = ""
        #there is no error
        return redirect("/tournamentView")
        #redirect to the in tournament view as tournament has been created
    elif len(tournamentName)<=4:
        session["tournamentCreationError"] = "Tournament name too short, must be over 4 characters"
        #if length of tournament name too short, this becomes error message
        return redirect("/creationForm")
        #reloads creationForm page with error displayed
    elif len(tournamentName)>=30:
        session["tournamentCreationError"] = "Tournament name too long, must be under 30 characters"
        #if length of tournament name too long, this becomes error message
        return redirect("/creationForm")
        #reloads creationForm page with error displayed
    else:
        session["tournamentCreationError"] = "Tournament name already taken"
        #only other possible error is that tournament name is already taken so this becomes error message
        return redirect("/creationForm")
        #reloads creationForm page with error displayed
        
