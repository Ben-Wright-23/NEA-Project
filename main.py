### Imports ###
from flask import Flask
from database import DatabaseHandler
from routes.userManagement import signupBlueprint, createUserBlueprint


app = Flask(__name__)
#Creates an instance of flask to register blueprints to
app.config["SECRET_KEY"] = "q7)p4ZV{X2R'P5F$W/eJ!rH;=u3h`}s5DavB8[dn"
#Can be used in any encryption/security being used
db = DatabaseHandler("appData.db")
#creates a link to the database
# db.createTables()
#creates the user entity, only run once then line removed

# db.dropUsers()
#Drops user table, used for testing


### Routing ###

app.register_blueprint(signupBlueprint)
#registers the signupBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(createUserBlueprint)
#registers the createUserBlueprint in the Flask instance so it can be used when running the program in the web framework





app.run(debug = True)