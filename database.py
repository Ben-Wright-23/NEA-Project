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


    # def dropUsers(self):
    #     connection = sql.connect(self.name)

    #     connection.execute("""DROP TABLE user;""")
        
    #     connection.close()
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
                    FOREIGN KEY (username) REFERENCES user(username)
                    CHECK (length(TournamentName)>4 AND length(TournamentName)<30)
                            );""")
        #execute previously designed sql statement on the database connection
        #active and bracket fields added to the database
        connection.close()
        #close the database connection

    def createTournament(self, tournamentName, username, numTeams, bracket):
        #define the function
        connection = sql.connect(self.name)
        #Connect to the database
        try:
            #use try except loop to be able to handle errors
            connection.execute("""INSERT INTO tournament
                VALUES (?,?,?,false,?)""",
                (tournamentName,username,numTeams,bracket)
                )
            #execute previously designed sql statement on the database connection
            #whn adding the active and bracket fields, this SQL had to be updated too to allow data for these fields to be added to the tournament 
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
                               SET bracket = ?
                               WHERE tournamentName = ?
                               """,(bracket, tournamentName))
            #execute the previously designed SQL statement
            connection.commit()
            #commit the changes to the database
            connection.close()
            #close the connection to the database
            return True
            #if there have been no errors, the function will return True
        except:
            connection.close()
            return False
            #if gthere was an error in the function, the connection will be closed and the function will return False
            

    def getBrackets(self,tournamentName):
        #defines get bracket function
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