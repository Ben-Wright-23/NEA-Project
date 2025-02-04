### Imports ###
from flask import Flask
from database import DatabaseHandler
from routes.home import homeBlueprint
from routes.dashboard import dashboardBlueprint
from routes.userManagement import signupBlueprint, createUserBlueprint, authenticateUserBlueprint, deleteAccountBlueprint, deleteUserBlueprint, logoutBlueprint
from routes.tournamentCreation import creationFormBlueprint, tournamentCreationBlueprint, teamsInputPageBlueprint,teamsInputBlueprint ,teamDeletionBlueprint, clearTeamsBlueprint


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

db.createTournamentTables()
#creates the tournament entity, only run once then line removed

### Routing ###
app.register_blueprint(signupBlueprint)
#registers the signupBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(createUserBlueprint)
#registers the createUserBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(homeBlueprint)
#registers the homeBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(authenticateUserBlueprint)
#registers the authenticateUserBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(deleteAccountBlueprint)
#registers the deleteAccountBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(deleteUserBlueprint)
#registers the deleteUserBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(logoutBlueprint)
#registers the logoutBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(dashboardBlueprint)
#registers the dashboardBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(creationFormBlueprint)
#registers the creationForm in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(tournamentCreationBlueprint)
#registers the tournamentCreation in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(teamsInputPageBlueprint)
#registers the teamsInputPageBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(teamsInputBlueprint)
#registers the teamsInputBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(teamDeletionBlueprint)
#registers the teamDeletionBlueprint in the Flask instance so it can be used when running the program in the web framework
app.register_blueprint(clearTeamsBlueprint)
#registers the clearTeamsBlueprint in the Flask instance so it can be used when running the program in the web framework

app.run(debug = True)