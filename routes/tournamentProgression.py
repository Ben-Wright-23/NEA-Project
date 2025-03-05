from flask import Blueprint,render_template, session, request,redirect
from database import DatabaseHandler
from datetime import time, timedelta,datetime
#imports the time and time delta functions from the datetime module so times the fixtures can add set lengths of times to a time
import math
#to allow log2 to be used to calculate the number of rounds in the tournament


fixturesPageBlueprint = Blueprint("fixturesPage",__name__)
#create a flask blueprint for the function to load the fixtures page
liveBracketViewPageBlueprint = Blueprint("liveBracketViewPage",__name__)
#create a flask blueprint for the function to load the live bracket view page
scoresInputPageBlueprint = Blueprint("scoresInputPage",__name__)
#create a flask blueprint for the function to load the scores input page
fixtureInfoInputBlueprint = Blueprint("fixtureInfoInput",__name__)
#create a flask blueprint for the function to load hhandle the user inputs to the fixture info input page and add the calculated fixture information to the database
fixtureInfoInputPageBlueprint = Blueprint("fixtureInfoInputPage",__name__)
#create a flask blueprint for the function to load the fixture info input page
scoresInputBlueprint = Blueprint("scoresInput",__name__)
#create a flask blueprint for the function to handle the user's score inputs and add these scores to the database, assigned to the correct matches


@liveBracketViewPageBlueprint.route("/liveBracketViewPage")
#creates the route for the liveBracketViewPage blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def liveBracketViewPage():
    #defines liveBracketViewPage function for the liveBracketViewPage blueprint
    return render_template("liveBracketView.html")
    #loads the live bracket view page

@fixturesPageBlueprint.route("/fixturesPage")
#creates the route for the fixturesPage blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def fixturesPage():
    #defines fixturesPage function for the fixturesPage blueprint
    session["FixtureInfoInputError"] = ""
    #clears the session containing errors with fixture information inputs so they are not already present from other tournaments when the fixture information input page is loaded
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of fields from the database for the current tournament 
    brackets = results[4]
    #sets brackets to be the fith value from the fields list as this represents that tournament's brackets
    brackets = eval(brackets)
    #turns the brackets back to their origional dictionary form
    roundStartTimes = results[6]
    #sets roundStartTimes to be the seventh value from the fields list as this represents that tournament's round start times
    roundStartTimes = eval(roundStartTimes)
    #turns the brackets back to their origional list form
    matchDuration = int(results[7])
    #sets matchDuration to be the integer version of the eighth value from the fields list as this represents that tournament's match duration
    breakLength = int(results[8])
    #sets breakLength to be the integer version of the ninth value from the fields list as this represents that tournament's length of breaks
    return render_template("fixtures.html", tournament = brackets, roundStartTimes = roundStartTimes, matchDuration = matchDuration, breakLength = breakLength)
    #loads the fixtures page, with the brackets passed in as tournament, round start times as roundStartTimes, match duration as matchDuration and break length as breakLength

@scoresInputPageBlueprint.route("/scoresInputPage")
#creates the route for the scoresInputPage blueprint, allowing it to be accessed easily.
def scoresInputPage():
    #defines scoresInputPage function for the scoresInputPage blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of fields from the database for the current tournament 
    brackets = results[4]
    #sets brackets to be the fifth value from the fields list as this represents that tournament's brackets
    brackets = eval(brackets)
    #turns the brackets back to its origional dictionary form
    matchScores = results[9]
    #sets matchScores to be the tenth value from the fields list as this represents that tournament's bracket with match scores added
    matchScores = eval(matchScores)
    #turns the matchScores back to their origional dictionary form
    return render_template("scoresInput.html", tournament = brackets, matchScores = matchScores)
    #loads the scores input page with the brackets and matchscores passed in so parts of them can be displayed


@fixtureInfoInputBlueprint.route("/fixtureInfoInput", methods = ["POST"])
#creates the route for the fixtureInfoInputBlueprint blueprint, allowing it to be accessed easily. Post method allows it to send data to the server
def fixtureInfoInput():
    #defines fixtureInfoInput function for the fixtureInfoInput blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of fields from the database for the current tournament 
    numTeams = results[2]
    #sets numTeams to be the third value from the fields list as this represents that tournament's number of teams
    numTeams = int(numTeams)
    #turns numTeams back to its integer version
    numRounds = int(math.log2(numTeams))
    #sets numRounds to be log2 of numTeams, as this finds the number of rounds the tournament will contain
    startTime = request.form["startTime"]
    #takes the entered tournament start time sent from the fixtureInfoInput page(the client) to the server, using the form input with name "startTime".
    matchDuration = request.form["matchDuration"]
    #takes the entered match duration sent from the fixtureInfoInput page(the client) to the server, using the form input with name "matchDuration".
    breakLength = request.form["breakLength"]
    #takes the entered break length sent from the fixtureInfoInput page(the client) to the server, using the form input with name "breakLength".
    if startTime[:2].isdigit() == False or int(startTime[:2])>23 or startTime[-2:].isdigit() == False or int(startTime[-2:])>59 or str(startTime)[2] != ":" or len(startTime)>5:
        #checks if the start time is in 24-hour clock format
        session["FixtureInfoInputError"] = "Entered tournament start time is not in the specified format"
        #if the start time is not in 24-hour clock format, there is an error so this session is set to this message to be displayed to the user so they can identify what they need to change with their inputs
        return redirect("/fixtureInfoInputPage")
        #redirects the user to the function to load the fixture info input page with this error displayed
    elif matchDuration.isdigit() == False:
        #checks the match duration is an integer
        session["FixtureInfoInputError"] = "Entered match duration is not an integer"
        #if the match duration is not an integer, there is an error so this session is set to this message to be displayed to the user so they can identify what they need to change with their inputs
        return redirect("/fixtureInfoInputPage")
        #redirects the user to the function to load the fixture info input page with this error displayed
    elif int(matchDuration) > 120:
        #checks if the integer version of the match duration is greater than 120 
        session["FixtureInfoInputError"] = "Entered match duration is too long"
        #if the match duration is longer than 120mins, there is an error as longer than this is unreasonable for a match so this session is set to this message to be displayed to the user so they can identify what they need to change with their inputs
        return redirect("/fixtureInfoInputPage")
        #redirects the user to the function to load the fixture info input page with this error displayed
    elif int(matchDuration) == 0:
        #checks if the integer version of the match duration is 0
        session["FixtureInfoInputError"] = "Entered match duration is not valid"
        #if the match duration is 0, there is an error as no match would take place so this session is set to this message to be displayed to the user so they can identify what they need to change with their inputs
        return redirect("/fixtureInfoInputPage")
        #redirects the user to the function to load the fixture info input page with this error displayed
    else:   
        #if no error has occured with the user's inputs
        session["FixtureInfoInputError"] = ""
        #there is no error so no error should be displayed
        addedTimePerRound = int(matchDuration)+int(breakLength)
        #sets the time to be added for eveery round that takes place to be the match duration + break length as this is the difference between the start times of adjacent matches
        userGivenTime = startTime.split(":")
        #creates a 2 item list, with the first item being the hours section of the user given start time and the second item being the minutes part
        hours = int(userGivenTime[0])
        #sets the hours part of the start time to be this value from the given time from the user
        mins = int(userGivenTime[1])
        #sets the minutes part of the start time to be this value from the given time from the user
        tournamentStartDateTime = datetime(2000,1,1,hours,mins,0)
        #sets tournamentDateStartTime to be the datetime value of what the user entered for the tournament start time, with placeholder values for the day, month, year and seconds
        tournamentStartTime = tournamentStartDateTime.time()
        #sets tournamentStartTime to be the time function from the datetime module of the datetime format of the user's entered tournament start time, 
        #making it the 24-hour clock time the user entered with 0 seconds in the time format from the datetime module
        roundStartTimes = []
        #creates an empty list for the start times of each round of matches
        roundStartTimes.append(str(tournamentStartTime)[:5])
        #adds the hours and minutes part or the tournament start time to the list of round start times
        newDateTime = tournamentStartDateTime
        #sets newDateTime to be the start time of the tournament, so this variable can be used to calculate the start times of the next round(s)
        for i in range(numRounds-1):
            #loops the content numRounds - 1 times as the start time for each round will be calculated and added to the list except the first round's start time as this has already been added before the loop
            newDateTime = newDateTime + timedelta(minutes=addedTimePerRound)
            #sets new time to the the time of the round before + the gap between start times calculated by adding the match duration and length of breaks betweeen matches
            if newDateTime.day == 2:
                #checks if the new round start time will occur on the next day, as the placeholder day value is 1
                session["FixtureInfoInputError"] = "Tournament matches must all start on the same day"
                #if it does occur on the next day, there is an error as matches should start on the same day,
                #so this session is set to this message to be displayed to the user so they can identify what they need to change with their inputs
                return redirect("/fixtureInfoInputPage")
                #redirects the user to the function to load the fixture info input page with this error displayed
            newTime = newDateTime.time()
            #sets newTime to be the time function version of the full datetime version of the new round's start time so the 24-hour clock time can be extracted
            roundStartTimes.append(str(newTime)[:5])
            #extracts the 24-hour clock version of the round's start time and adds this value to the list of round start time
        db.addFixtureInfo(str(roundStartTimes), matchDuration, breakLength, session["Tournament"])
        #adds the string version of the list of round start times, match duration and length of breaks to the current tournament in the database
        return redirect("/fixturesPage")
        #redirect the user to the function to load fixtures page with this fixture information displayed 

@fixtureInfoInputPageBlueprint.route("/fixtureInfoInputPage")
#creates the route for the fixtureInfoInputPageBlueprint blueprint, allowing it to be accessed easily. 
def fixtureInfoInputPage():
    #defines fixtureInfoInputPage function for the fixtureInfoInputPage blueprint
    return render_template("fixtureInfoInput.html", error = session["FixtureInfoInputError"])
    #loads the Fixture Info Input html page, with any errors occured when completing the form on this page passed in to be displayed 

@scoresInputBlueprint.route("/scoresInput", methods = ["POST"])
#creates the route for the scoresInput blueprint, allowing it to be accessed easily.
def scoresInput():
    #defines scoresInput function for the scoresInput blueprint
    db = DatabaseHandler("appData.db")
    #creates a link to the database, where appData.db is the database storing the enities
    results = db.getTournamentFields(session["Tournament"])
    #sets results to be the list of fields from the database for the current tournament
    brackets = results[4]
    #sets brackets to be the fith value from the fields list as this represents that tournament's brackets
    brackets = eval(brackets)
    #turns the brackets back to their origional dictionary form
    team1Score = request.form["score1"]
    #takes the score the user has entered for the first team in the match and sets it to team1Score
    team2Score = request.form["score2"]
    #takes the score the user has entered for the second team in the match and sets it to team2Score
    roundMatch = request.form["match"]
    #takes the round and match the submit scores button has been round on, split by a comma
    roundMatch = roundMatch.split(",")
    #splits the round and match into a list, with the first item being the round and second the match
    round = int(roundMatch[0])
    #sets round to be the integer version of the first item in the round and match list, which is the round the user pressed the submit scores button in
    match = int(roundMatch[1])
    #sets match to be the integer version of the second item in the round and match list, which is the match the user pressed the submit scores button on
    team1 = brackets[round][match][1]
    #selects the team name of the first team in the match that has had submit scores button pressed on and sets it to team1
    team2 = brackets[round][match][2]
    #selects the team name of the second team in the match that has had submit scores button pressed on and sets it to team2
    teamScore1 = []
    #creates an empty list, called team score 1, that will store the team and that teams score in the match for the first team in the match
    teamScore1.append(team1)
    #append the first team of the match the submit scores button has been pressed on to the teamScore1 list
    teamScore1.append(team1Score)
    #append the first team of the match's score for the match that the submit scores button has been pressed on to the teamScore1 list
    teamScore2 = []
    #creates an empty list, called team score 2, that will store the team and that teams score in the match for the second team in the match
    teamScore2.append(team2)
    #append the second team of the match the submit scores button has been pressed on to the teamScore2 list
    teamScore2.append(team2Score)
    #append the second team of the match's score for the match that the submit scores button has been pressed on to the teamScore2 list
    matchScores = brackets
    #sets matchScores to be a copy of the brackets for the current tournament in the database
    matchScores[round][match][1] = teamScore1
    #sets the first item in the match that has had submit scores pressed on within the matchscores copy of brackets to be the teamScore 1 list, 
    #containing both the team name and its score in the match
    matchScores[round][match][2] = teamScore2
    #sets the second item in the match that has had submit scores pressed on within the matchscores copy of brackets to be the teamScore 2 list, 
    #containing both the team name and its score in the match
    db.addMatchScores(str(matchScores), session["Tournament"])
    #adds the string version of matchScores dictionary, containing the bracket + scores assigned to teams,
    #to the matchScores field in the current tournament in the database
    return redirect("/scoresInputPage")
    #redirects the user to the function to reload the scores input page
    