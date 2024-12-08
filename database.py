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