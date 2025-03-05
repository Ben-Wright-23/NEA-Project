import sqlite3 as sql



### Class ###
class DatabaseHandler:
    #defines the class
    def __init__(self, databaseName):
        self.name = databaseName
    #defines the constructor to make the object

    def createTables(self):
        #define a createTables function so it can be accessed easily
        connection = sql.connect(self.name)
        #connect to the created database
        connection.execute("""CREATE TABLE IF NOT EXISTS user(
                           
                           username text PRIMARY KEY,
                           password text NOT NULL,
                           CHECK ((length(password)>7 AND password GLOB '*[0-9]*') AND (length(username)>3 AND length(username)<16))

                           );""")
        #execute previously designed sql statement, execute it in the database connection to store it in the intended place
        connection.close()
        #close the database connection

    def createUser(self, username, password):
        #define a createUser function so it can be accessed easily, pass in the username and password the user has entered in the html page
        connection = sql.connect(self.name)
        #connect to the created database
        try:
            #use try except loop to be able to handle errors
            connection.execute("""INSERT INTO user
                            VALUES (?,?)""", (username,password))
            #execute previously designed sql statement, execute it in the database connection to store it in the intended place
            connection.commit()
            #commit the changes in the database to store fully, required as changes being made to the database
            connection.close()
            #close the database connection
            return True
            #Shows that the user has been added successfully when function called
        except:  
            #reverts to this if validation requirements not met                    
            connection.close()
            #close the database connection
            return False
            #Signals user has not been created successfully when function is called


    def dropUsers(self):
        connection = sql.connect(self.name)

        connection.execute("""DROP TABLE tournament;""")
        
        connection.close()
    #function used for testing

    def authenticateUser(self, username, password):
        #define the function to make it easily accessable, pass in the username and password entered it can be checked if they exist in the database or not
        connection = sql.connect(self.name)
        #connect to the created database
        cursor = connection.cursor()
        #create a cursor to inspect one row of the table at a time
        cursor.execute("""SELECT username 
                       FROM user
                       WHERE username = ? 
                       AND password = ? ;""",
                       (username,password))
        #execute previously designed sql statement, execute it in the cursor so the data can be fetched
        result = cursor.fetchone()
        #if the cursor has found a match for the inputted details, it stores it as the result
        connection.close()
        #close the database connection
        if result != None:
            return True
            #if the cursor successfully fetched a row with matching details, the function returns True to signify there is an account with the details the user entered
        else:
            return False
            #if cursor could not find an account with matching details to what the user entered, the function returns False
            

    def deleteUser(self,currentUser):
        #define the function
        connection = sql.connect(self.name)
        #Connect to the database
        connection.execute("""DELETE FROM user
                        WHERE username = ? ;""",
                        [currentUser])
        #execute previously designed sql statement on the database connection
        connection.commit()
        #commit the changes to the database so they are stored permaneantly
        connection.close()
        #close the database connection


    def createTournamentTables(self):
        #define the function
        connection = sql.connect(self.name)
        #Connect to the database
        connection.execute("""CREATE TABLE IF NOT EXISTS tournament(
                    tournamentName text PRIMARY KEY,
                    username text,
                    numTeams integer NOT NULL,
                    active text,
                    bracket text,
                    viewCode text,
                    roundStartTimes text,
                    matchDuration text,
                    breakLength text,
                    matchScores text,
                    FOREIGN KEY (username) REFERENCES user(username)
                    CHECK (length(TournamentName)>4 AND length(TournamentName)<30)
                            );""")
        #execute previously designed sql statement on the database connection
        #active and bracket fields added to the database
        #viewCode field added to the database
        #roundStartTimes, matchDuration and breakLength fields added to the database
        #matchScores field added to the database
        connection.close()
        #close the database connection

    def createTournament(self, tournamentName, username, numTeams, bracket):
        #define the function
        connection = sql.connect(self.name)
        #Connect to the database
        try:
            #use try except loop to be able to handle errors
            connection.execute("""INSERT INTO tournament
                               (tournamentName,username,numTeams,active,bracket)
                            VALUES (?,?,?,false,?)""",
                            (tournamentName,username,numTeams,bracket)
                            )
            #execute previously designed sql statement on the database connection
            #when adding the active and bracket fields, this SQL had to be updated too to allow data for these fields to be added to the tournament 
            #line 2 in the statement inserts the values into these specific fields, so it can ignore any other fields when inserting 
            connection.commit()
            #commit the changes to the database so they are stored permaneantly
            connection.close()
            #close the database connection
            return True
            #Shows that the tournament has been added successfully when function called
        except:
            #reverts to this if validation requirements not met  
            connection.close()
            #close the database connection
            return False
            #Signals tournament has not been created successfully when function is called

    def addBrackets(self, bracket, tournamentName):
        #defines add bracket function
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET bracket = ?, matchScores = ?
                               WHERE tournamentName = ?
                               """,(bracket, bracket, tournamentName))
            #execute the previously designed SQL statement
            #adds the brackets to the match scores field too so it has a base store of all the matches so the scores can be added to them
            connection.commit()
            #commit the changes to the database
            connection.close()
            #close the connection to the database
            return True
            #if there have been no errors, the function will return True
        except:
            connection.close()
            return False
            #if there was an error in the function, the connection will be closed and the function will return False
            

    def getTournamentFields(self,tournamentName):
        #defines get bracket function
        #name changed to getTournamentFields to better suit its multiple purposes
        try:
            connection = sql.connect(self.name)
            #connect to the database
            cursor = connection.cursor()
            #create a cursor to inspect one row of the table at a time
            cursor.execute("""SELECT * FROM tournament WHERE tournamentName = ?;""",[tournamentName])
            #exectute the previously designed SQL statement using the cursor to check through the records
            results = cursor.fetchone()
            #fetch the record with the current tournament's name
        except Exception as e:
            print(e)
            results = {}
            #if there has been an error in the "try", this error is printed and there is no record to be returned
        finally:
            connection.close()
            #close the connection to the database
            return results
            #return the whole record of the user's current tournament


    def updateActiveTrue(self, tournamentName):
        #defines update active function
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET active = ?
                               WHERE tournamentName = ?
                               """,("true", tournamentName))
            #exectute the previously designed SQL statement
            connection.commit()
            #commit the changes to the database
            connection.close()
            #close the connection to the database
            return True
            #if no errors have occured, the function will return true
        except:
            connection.close()
            #close the connection to the database
            return False
            #if there has been an error, the function returns false

            
    def checkViewCodes(self,viewCode):
        #defines checkViewCodes function, with the view code to be checked for passed in
        try:
            connection = sql.connect(self.name)
            #connect to the database
            cursor = connection.cursor()
            #creates a cursor to inspect one row of the table at a time
            cursor.execute("""SELECT viewCode FROM tournament WHERE viewCode = ?;""",[viewCode])
            #exectutes the previously designed SQL statement using the cursor to check through the records for the view code has been passed in
            results = cursor.fetchone()
            #fetches the view code if there is one that matches the passed in view code
            connection.close()
            #close the connection to the database
            return results
            #returns the view code if it is already present in the database, making it not a unique view code, otherwise it will return None
        except Exception as e:
            #if there was an error executing the SQL statement:
            connection.close()
            #close the connection to the database
            print(e)
            #print the error that has occured
            return False
            #returns false signifying the check has not been completed
            
    def addViewCode(self, viewCode, tournamentName):
        #defines checkViewCodes function, with the view code to be added passed in as well as the tournament it should be assigned to
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET viewCode = ?
                               WHERE tournamentName = ?
                               """,(viewCode, tournamentName))
            #exectutes the previously designed SQL statement to add the view code to the current tournament
            connection.commit()
            #commit the addition of the view code to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the viewCode has been added to the current tournament successfully
        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns true signifying the viewCode has not been added to the current tournament successfully


    def getTournaments(self,currentUser):
        #defines getTournaments function, the current user trying to access their tournaments passed in
        try:
            connection = sql.connect(self.name)
            #connect to the database
            cursor = connection.cursor()
            #creates a cursor to inspect one row of the table at a time
            cursor.execute("""SELECT * FROM tournament WHERE username = ?;""",[currentUser])
            #exectutes the previously designed SQL statement to select all tournaments where the username matches the given current user
            results = cursor.fetchall()
            #fetches all the tournaments that have a username matching the passed in username for the current user 
            connection.close()
            #close the connection to the database
            return results
            #returns all the tournaments and all the data in their fields, where the tournament's username matches the given current user
        except Exception as e:
            connection.close()
            #close the connection to the database
            print(e)
            #print the error in the SQL statement if there has been one
            return False
            #returns false signifying the selection was unsuccessful
            
    def deleteTournament(self,tournamentName):
        #defines deleteTournament function, with the tournament name of the tournament that needs to be deleted passed in
        connection = sql.connect(self.name)
        #connect to the database
        connection.execute("""DELETE FROM tournament
                            WHERE tournamentName = ? ;""",
                            [tournamentName])
        #exectutes the previously designed SQL statement to delete the tournament with a given tournament name
        connection.commit()
        #commit the deletion of the tournament to the database
        connection.close()
        #close the connection to the database

    def addFixtureInfo(self, startTimes, duration, breakLength, tournamentName):
        #defines addFixtureInfo function, with the round start times, match duration and break length to be added passed in as well as the tournament they should be assigned to
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET roundStartTimes = ?, matchDuration = ?, breakLength = ?
                               WHERE tournamentName = ?;
                               """,(startTimes,duration,breakLength,tournamentName))
            #exectutes the previously designed SQL statement to add the round start times, match duration and break length to the current tournament
            connection.commit()
            #commit the addition of the round start times, match duration and break length to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the round start times, match duration and break length have been added to the current tournament successfully
        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns true signifying the round start times, match duration and break length have not been added to the current tournament successfully

    def addMatchScores(self, matchScores, tournamentName):
        #defines addMatchScores function, with the match scores to be added passed in as well as the tournament they should be assigned to
        try:
            connection = sql.connect(self.name)
            #connect to the database
            connection.execute("""UPDATE tournament 
                               SET matchScores = ?
                               WHERE tournamentName = ?;
                               """,(matchScores,tournamentName))
            #executes the previously designed SQL statement to add the match scores to the current tournament
            connection.commit()
            #commit the addition of the match scores to the database
            connection.close()
            #close the connection to the database
            return True
            #returns true signifying the match scores have been added to the current tournament successfully
        except:
            #if there has been an error in the SQL statement
            connection.close()
            #close the connection to the database
            return False
            #returns false signifying the match scores have not been added to the current tournament successfully

