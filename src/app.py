from flask import Flask
from routes.user import user_register
from routes.control import baseControl
app = Flask(__name__)

#this is a secret key
app.secret_key = 'password123'

@app.route('/')
def index():
    return 'Hello World'

app.register_blueprint(user_register)
app.register_blueprint(baseControl)

if __name__ == '__main__':
    app.run(debug=True)