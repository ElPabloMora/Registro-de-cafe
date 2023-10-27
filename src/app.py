from flask import Flask
from routes.user import user_register
from routes.control import baseControl
from flask_login import LoginManager
from Models.modelUser import ModelUser
from Database.database import connect_base
app = Flask(__name__)

connect = connect_base()
#this is a secret key
app.secret_key = 'password123'

app.register_blueprint(user_register)
app.register_blueprint(baseControl)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(connect,id)

if __name__ == '__main__':
    app.run(debug=True)