from flask import Blueprint,render_template, session, request, redirect
from database import DatabaseHandler
# import database and required flask modules
import math
#import math module so log2 can be performed for number of rounds
import random
#so randint can be used when generating the view code

creationFormBlueprint = Blueprint("creationForm",__name__)
#create a flask blueprint for the function to load the tournamentCreation page
tournamentCreationBlueprint = Blueprint("tournamentCreation",__name__)
#create a flask blueprint for the function to link the interface and database for the tournament creation and to display errors with the tournament creation
teamsInputPageBlueprint = Blueprint("teamsInputPage",__name__)
#create a flask blueprint for the function to load the teamsInput page
teamsInputBlueprint = Blueprint("teamsInput",__name__)
#create a flask blueprint for the function to add teams to the tournament as long as the entered data from the user is valid
teamDeletionBlueprint = Blueprint("teamDeletion",__name__)
#create a flask blueprint for the function to individually delete teams depending on the users input
clearTeamsBlueprint = Blueprint("clearTeams",__name__)
#create a flask blueprint for the function to remove all teams from the tournament
bracketViewBlueprint = Blueprint("bracketView",__name__)
#create a flask blueprint for the function to load the bracket viewing page
bracketGenerationBlueprint = Blueprint("bracketGeneration",__name__)
#create a flask blueprint for the function create the bracket dictionary and add it to the database with its corresponding tournament
bracketDisplayBlueprint = Blueprint("bracketDisplay",__name__)
#create a flask blueprint for the function to retreive the bracket from the database
tournamentDashboardBlueprint = Blueprint("tournamentDashboard",__name__)
#create a flask blueprint for the function to load the tournament dashboard
generateViewCodeBlueprint = Blueprint("generateViewCode",__name__)
#create a flask blueprint for the function to load generate the unique view code and add it to the database
myTournamentsPageBlueprint = Blueprint("myTournamentsPage",__name__)
#create a flask blueprint for the function to load the my tournaments page with all the current user's tournaments displayed
tournamentDashboardRedirectBlueprint = Blueprint("tournamentDashboardRedirect",__name__)
#create a flask blueprint for the function to redirect the user directly to the tournament dashboard when the "Go to Tournaments" button is pressed
deleteTournamentBlueprint = Blueprint("deleteTournament",__name__)
#create a flask blueprint for the function to delete a selected tournament from the database and my tournaments page
teamsInputRedirectBlueprint = Blueprint("teamsInputRedirect",__name__)
#create a flask blueprint for the function to redirect the user to the teams input page if their tournament was up to this stage of creation and the "Go to Teams Input" button is pressed
bracketViewRedirectBlueprint = Blueprint("bracketViewRedirect",__name__)
#create a flask blueprint for the function to redirect the user to the bracket view page if their tournament was up to this stage of creation and the "Go to Bracket View" button is pressed



@creationFormBlueprint.route("/creationForm")
#creates the route for the creationForm blueprint, allowing it to be accessed easily
def creationForm():
    #defines function to load creationForm page
    session["teamInputError"] = ""
    #resets any errors possibly still being displayed from previous tournaments
    session["teamDeletionError"] = ""
    #resets any team deletion errors possibly still being displayed from previous tournaments
    Error = session.get("tournamentCreationError") if session.get("tournamentCreationError") else ""
    #produces the error with the tournament creation if there is one
    #if no error, no error is passed to the interface
    return render_template("creationForm.html", error = Error)
    #loads the creationForm.html page, with the error message displayed when it is reloaded


@tournamentCreationBlueprint.route("/tournamentCreation", methods = ["POST"])
#creates the route for the tournamentCreation blueprint, allowing it to be accessed easily. Post method allows it to make server side changes
def tournamentCreation():
    #defines function to load creationForm page
    session["Teams"] = ""
    #Resets the teams list displayed to the user from any previous tournaments
    teams.clear()
    #removes all teams from the back end so there is no carry over from other tournaments
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database and where the entities will be stored
    tournamentName = request.form["tournamentName"]
    #takes the entered tournamentName part of the data sent from the creationForm page(the client) to the server, using the form input with id "tournamentName".
    global numTeams
    #numTeams is required multiple times through this file so making it a global variable is a suitable method to allow other functions to access it
    numTeams = request.form["numTeams"]
    #takes the entered number of teams part of the data sent from the creationForm page(the client) to the server, using the form input with id "numTeams".
    numTeams = int(numTeams)
    #numTeams made an integer
    session["Tournament"] = tournamentName
    #makes a session for the current tournament's name

    if db.createTournament(tournamentName,session["currentUser"],numTeams,None)==True:
        #if the tournament is created successfully
        #None added to act as a placeholder for the bracket to be added later
        session["tournamentCreationError"] = ""
        #there is no error
        return redirect("/teamsInputPage")
        #redirect to the in teams input page to continue creating the tournament
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
        
teams=[]
#Creates the back-end list that will contain all teams currently in the tournament
@teamsInputPageBlueprint.route("/teamsInputPage")
#creates the route for the teamsInputPage blueprint, allowing it to be accessed easily
def teamsInputPage():
    #defines function to load teamsInputPage
    Error = session.get("teamInputError") if session.get("teamInputError") else ""
    DeletionError = session.get("teamDeletionError") if session.get("teamDeletionError") else ""
    #Produces the errors with the team inputting or deleting if there is one
    #if no error for either, no error is passed for that error to the interface
    return render_template("teamsInput.html", error = Error, error2 = DeletionError)
    #loads the creationForm.html page, with the error messages displayed when it is reloaded

@teamsInputBlueprint.route("/teamsInput", methods = ["POST"])
#creates the route for the teamsInput blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def teamsInput():
    #defines teamsInput function   for the teams input blueprint
    if len(teams)<int(numTeams):
        #creates condition to check there is less teams in the list/tournament than the user previously specified was how many teams their tournament would contain
        newTeamName = request.form["teamNames"]
        #takes the entered team name sent from the teamsInput page(the client) to the server, using the form input with id "teamNames".
        for i in teams:
            #cycles through all team names in the list of team names
            if newTeamName==i:
                #compares the new team name with all team names currently in the list
                session["teamInputError"] = "Teams must have unique name"
                #If there is a matching team name in the list, there is an error with the team input so this session is set to this message to be displayed to the user
                return redirect("/teamsInputPage")
                #reloads the team input page with the error displayed
        if newTeamName != "":
            #Checks the user has entered a value for the team name
            teams.append(newTeamName)
            #adds the new team to the list of teams if there is a team name entered
            session["Teams"] = teams
            #Update the session for teams to be the new list of teams so it can be displayed to the user in the teamsInput html page
            session["teamInputError"] = ""
            #The team entered is valid so there is no error with the team input
            return redirect("/teamsInputPage")
            #Reloads the teamInput page with the new team added to the list displayed to the user
        else:
            session["teamInputError"] = "Team must have a name"
            #If no name for the team entered, output an error message stating this
            return redirect("/teamsInputPage")
            #Reloads the teamInput page with the error displayed to the user
    else:
        session["teamInputError"] = "Your amount of teams has been reached"
        #If there are as many teams in the list as that the user has said their tournament should contain, the new team is not entered and this error is displayed
        return redirect("/teamsInputPage")
        #Reloads the teamInput page with the error displayed to the user

@teamDeletionBlueprint.route("/teamDeletion", methods = ["POST"])
#creates the route for the teamDeletion blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def teamDeletion():
    #defines teamsDeletion function for the team deletion blueprint
    toDelete = request.form["teamDeletion"]
    #takes the entered team name to be deleted sent from the teamsInput page(the client) to the server, using the form input with id "teamDeletion".
    for i in teams:
        if i == toDelete:
            #Cycles through every team in the list, checking if it matches the name of the team to be deleted
            teams.remove(toDelete)
            #Removes the entered team name from the teams list and therefore tournament
            session["Teams"] = teams
            #Update the session for teams to be the new list of teams so it can be displayed to the user in the teamsInput html page
            session["teamDeletionError"] = ""
            #The team has been deleted successfully so there is no error with the team deletion
        else:
            session["teamDeletionError"] = "Team not in tournament"
            #If the team name has not been found in the list, the team is not in the tournament so this error is displayed to the user
    
    return redirect("/teamsInputPage")
    #Reloads the teams input page with any errors or changes to the team list

@clearTeamsBlueprint.route("/clearTeams", methods = ["POST"])
#creates the route for the clearTeams blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def clearTeams():
    #defines clearTeams function for the clearTeams blueprint
    teams.clear()
    #Clears all teams from the team list
    session["Teams"] = teams
    #Updates the session for teams to be empty, matching the teams list
    return redirect("/teamsInputPage")
    #Reloads the teamsInput page with all teams removed from the list


@bracketViewBlueprint.route("/bracketView")
#creates the route for the bracketView blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def bracketView():
    #defines bracket view function for the bracketView blueprint
    if len(teams)< numTeams:
        #if the user entered less teams to the teams list than they specified the number of teams in their tournament would be:
        session["teamInputError"] = "Not enough teams entered" 
        #there is a team input error that not enough teams have been entered
        return redirect("/teamsInputPage")
        #reload the team input page with this error displayed
    else:
        #otherwise, there is no error
        generateBrackets()
        # when the page is loaded, this generates the brackets annd adds them to the database
        return render_template("bracketView.html", brackets = bracketDisplay(), numberOfRounds = int(math.log2(numTeams)))
        #Loads the bracketView html page with the brackets and number of rounds passed in

@bracketGenerationBlueprint.route("/bracketGeneration")
#creates the route for the bracketGeneration blueprint, allowing it to be accessed easily.
def generateBrackets():
    #defines generateBrackets function for the bracketGeneration blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database and where the entities will be stored
    teamsList = teams
    #creates a copy of the "teams" list to be used within the function as otherwise teams would be changed and not be able to be used in other functions
    numberOfTeams = numTeams
    #creates a copy of the numTeams to be used in the function as otherwise numTeams would be changed and not be able to be used in other functions
    numRounds = int(math.log2(numberOfTeams))
    #sets the number of rounds to be log2 of the number of teams as this is how a the number of rounds in a bracket tournament like this is determined
    bracket = {}
    #creates an initially blank dictionary for the bracket

    for i in range(numRounds):
        #for however many rounds there are:
        round = {}
        #creates a blank dictionary for each round in the tournamnet
        bracket[i+1]= round
        #inputs each round dictionary into the bracket dictionary, assigning the first round with number 1 and so on
        numMatches = numberOfTeams // 2
        #each match has 2 teams so number of matches is half the number of teams
        for i in range(numMatches):
            round[i+1] = {1:None, 2:None}
            #for however many matches there will be in each round, this sets the match in each round to this match dictionary, containing team 1 and team 2 which have not yet been assigned
        numberOfTeams = numberOfTeams // 2
        #halfs the number of teams each time a round is made, as half teams will be eliminated each round

    for i in range (numTeams//2):
        #for however many matches there are in the first round:
        team1 = teamsList.pop(0)
        #the first team in the match is the first team in the teams list
        team2 = teamsList.pop(0)
        #the second team in the match is the new first team in the teams list after the first team has been removed as it is popped
        bracket[1][i+1][1] = team1
        #In the first round of the bracket, the first team in each match in turn is set to the first team in the remaining teams list
        bracket[1][i+1][2] = team2
        #In the first round of the bracket, the second team in each match in turn is set to the new first team in the remaining teams list after team1 is popped

    return db.addBrackets(str(bracket), session["Tournament"])
    #this functions return adds the brackets dictionary to the bracket field as a string into the tournament with the current tournament's name

@bracketDisplayBlueprint.route("/bracketDisplay")
#creates the route for the bracketDisplay blueprint, allowing it to be accessed easily.
def bracketDisplay():
    #defines bracketDisplay function for the bracketDisplay blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournamentFields(session["Tournament"])
    #retrieves the record of the current tournament from the database
    brackets = (results[4])
    #sets brackets to be the bracket field from the record containing all the info about the current tournament
    brackets = eval(brackets)
    #turns the string version of the brackets that is stored in the database back to its origional dictionary form
    return brackets
    #returns the dictionary version of the brackets

    
@tournamentDashboardBlueprint.route("/tournamentDashboard")
#creates the route for the tournamentDashboard blueprint, allowing it to be accessed easily.
def tournamentDashboard():
    #defines tournamentDashboard function for the tournamentDashboard blueprint
    session["FixtureInfoInputError"] = ""
    #defines the FixtureInfoInputError session or clears the session containing errors with fixture information inputs so they are not already present from other tournaments when the fixture information input page is loaded
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    db.updateActiveTrue(session["Tournament"])
    #updates the active field to be true in the database for the current tournament signifying the tournament has started
    results = db.getTournamentFields(session["Tournament"])
    #retrieves all the fields for the current tournament and sets the list retrieved to be results
    viewCode = results[5]
    #sets viewCode to be the sixth item in the list of current tournament fields as this represents the view code
    viewCode = eval(viewCode)
    #turns the view code back to its origional string form
    if results[6] != None:
        #if the seventh item of results is not None, this signifies the fixture information for the tournament has already been inputted 
        fixturesInfoInputted="True"
        #sets fixturesInfoInputted to be True to signify the fixture information for the tournament has already been inputted so the fixtures page should be loaded if the Fixtures button is pressed on the tournament dashboard
    else:
        #if the seventh item of results is None, this signifies the fixture information for the tournament has not already been inputted
        fixturesInfoInputted="False"
        #sets fixturesInfoInputted to be False to signify the fixture information for the tournament has not already been inputted so the fixture info input page should be loaded if the Fixtures button is pressed on the tournament dashboard
    return render_template("tournamentDashboard.html", viewCode = viewCode, fixturesInfoInputted = fixturesInfoInputted)
    #loads the tournament dashboard, with the specific tournament's view code passed in as viewCode so it can be displayed
    #also passes in whether the fixture information has been inputted yet so the program can choose whether the fixture info input page should be loaded or the fixtures page should be loaded when the Fixtures button is pressed


@generateViewCodeBlueprint.route("/generateViewCode")
#creates the route for the generateViewCode blueprint, allowing it to be accessed easily.
def generateViewCode():
    #defines generateViewCode function for the generateViewCode blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = "notnone"
    #sets the results local variable to be a value that is not None so the while loop begins 
    while results != None:
        #If the return from the database check for the new view code is not None, the new view code is already being used in the database. 
        #This means a new view code should be generated and checked for in the database so the while loop should continue
        viewCode = str(random.randint(100000,999999))
        #generates a random 6 digit number, makes it a string and assigns it to the variable viewCode
        results = db.checkViewCodes(viewCode)
        #assigns the return from the checkViewCodes database function when this 6 digit string is checked for and assigns it to the results variable
        

    db.addViewCode(viewCode, session["Tournament"])
    #Once a unique view code is generated, this line calls the database function to add it to the database, assigning it to the current tournament

    return redirect ("/tournamentDashboard")
    # redirect the user to the tournament dashboard page once the view code for the tournament has been added to the database


@myTournamentsPageBlueprint.route("/myTournamentsPage")
#creates the route for the myTournamentsPage blueprint, allowing it to be accessed easily.
def myTournamentsPage():
    #defines myTournamentsPage function for the myTournamentsPage blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournaments(session["currentUser"])
    #sets results to be all of the current user's tournaments, including all the fields in each tournament, formatted as lists within a list
    return render_template("myTournaments.html", tournaments = results)
    #loads the my tournaments html page, with all the current user's tournaements passed in as "tournaments" so they and the fields within them can be displayed


@tournamentDashboardRedirectBlueprint.route("/tournamentDashboardRedirect", methods = ["POST"])
#creates the route for the tournamentDashboardRedirect blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def tournamentDashboardRedirect():
    #defines tournamentDashboardRedirect function for the tournamentDashboardRedirect blueprint
    session["FixtureInfoInputError"] = ""
    #defines the FixtureInfoInputError session or clears the session containing errors with fixture information inputs so they are not already present from other tournaments when the fixture information input page is loaded
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    session["Tournament"] = request.form["tournamentName"]
    #sets the Tournament session to be the tournament name value of the tournament that has been clicked on on the myTournaments html page
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of all fields for the tournament with the name of the value in the tournament session
    viewCode = results[5]
    #sets viewCode to be the sixth item from this list as represents the tournament's view code
    viewCode = eval(viewCode)
    #turns the view code back to its origional string form
    if results[6] != None:
        #if the seventh item of results is not None, this signifies the fixture information for the tournament has already been inputted 
        fixturesInfoInputted="True"
        #sets fixturesInfoInputted to be True to signify the fixture information for the tournament has already been inputted so the fixtures page should be loaded if the Fixtures button is pressed on the tournament dashboard
    else:
        #if the seventh item of results is None, this signifies the fixture information for the tournament has not already been inputted
        fixturesInfoInputted="False"
        #sets fixturesInfoInputted to be False to signify the fixture information for the tournament has not already been inputted so the fixture info input page should be loaded if the Fixtures button is pressed on the tournament dashboard
    return render_template("tournamentDashboard.html", viewCode = viewCode, fixturesInfoInputted = fixturesInfoInputted)
    #loads the tournament dashboard, with the specific tournament's view code passed in as viewCode so it can be displayed
    #also passes in whether the fixture information has been inputted yet so the program can choose whether the fixture info input page should be loaded or the fixtures page should be loaded when the Fixtures button is pressed


@deleteTournamentBlueprint.route("/deleteTournament", methods = ["POST"])
#creates the route for the deleteTournament blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def deleteTournament():
    #defines deleteTournament function for the deleteTournament blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    tournamentToDelete = request.form["deleteTournament"]
    #set tournamentToDelete to be the tournament name of the tournament the "delete tournament" button was selected on on the my tournaments page
    db.deleteTournament(tournamentToDelete)
    #delete the tournament with this tournament name from the database
    return redirect("/myTournamentsPage")
    #redirect the user to the function to load the my tournaments page so it reloads without this tournament present

@teamsInputRedirectBlueprint.route("/teamsInputRedirect", methods = ["POST"])
#creates the route for the teamsInputRedirect blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def teamsInputRedirect():
    #defines teamsInputRedirect function for the teamsInputRedirect blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    session["Teams"] = ""
    #clears the teams session so the teams input page appears blank
    teams.clear()
    #clears the teams list so the teams input page appears blank
    session["teamDeletionError"] = ""
    #clears the team deletion error session so the teams input page appears blank
    session["teamInputError"] = "" 
    #clears the team input error session so the teams input page appears blank
    session["Tournament"] = request.form["tournamentName"]
    #sets the Tournament session to be the tournament name value of the tournament that has been clicked on on the myTournaments html page
    results = db.getTournamentFields(session["Tournament"])
    #retrieves all the fields for the current tournament being dealt with
    global numTeams
    # makes the numTeams variable global so all functions can access it
    numTeams = results[2]
    #sets the numTeams variable to the third item in the list of fields for the current tournament as this represents the number of teams for the tournament
    numTeams = int(numTeams)
    #turns numTeams back to its origional integer form
    return redirect("/teamsInputPage")
    #redirects the user to the function to load the teams input page

@bracketViewRedirectBlueprint.route("/bracketViewRedirect", methods = ["POST"])
#creates the route for the bracketViewRedirect blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def bracketViewRedirect():
    #defines bracketViewRedirect function for the bracketViewRedirect blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    session["Tournament"] = request.form["tournamentName"]
    #sets the Tournament session to be the tournament name value of the tournament that has been clicked on on the myTournaments html page
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of fields from the database for the tournament with the tournament name of the value in the tournament session
    global numTeams
    #sets the numTeams variable global so any future functions needed can use the correct number of teams for the current tournament being dealt with
    numTeams = results[2]
    #sets numTeams to be the third value from the fields list as this represents that tournament's number of teams
    numTeams = int(numTeams)
    #turns the number of teams value from the database back to its integer form
    brackets = results[4]
    #sets brackets to be the fith value from the fields list as this represents that tournament's brackets
    brackets = eval(brackets)
    #turns the brackets back to their origional dictionary form
    return render_template("bracketView.html", brackets = brackets, numberOfRounds = int(math.log2(numTeams)))
    #loads the bracket view html page with the brackets for the tournament selected and number of rounds, which is derrived from the number of teams of the selected tournament, passed in with the page

    