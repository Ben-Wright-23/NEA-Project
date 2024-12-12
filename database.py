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
                           CHECK ((length(password)>6 AND password GLOB '*[0-9]*') AND (length(username)>3 AND length(username)<16))

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
            #Signals user has not been created succefully when function is called


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
                        (currentUser))
        #execute previously designed sql statement on the database connection
        connection.commit()
        #commit the changes to the database so they are stored permaneantly
        connection.close()
        #close the database connection