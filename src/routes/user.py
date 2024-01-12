from flask import Blueprint, render_template, flash, redirect, url_for, request
from Database.database import connect_base
from werkzeug.security import generate_password_hash
from Models.userg import User
from Models.modelUser import ModelUser
from flask_login import login_user , logout_user

conect = connect_base()
cursor =conect.cursor()



user_register = Blueprint('user_register',__name__)


@user_register.route('/')
def index():
    return render_template('home.html')



@user_register.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if username != '' and email != '' and password != '':
            #use werkzeug for generate password hash
            password_hash = generate_password_hash(password,'sha256')
            #here use "fusion" to combine names
            fusion=str(username+password)           
            #here use func hash
            nameDB= generate_password_hash(fusion,'sha256')
            #All db
            cursor.execute('INSERT INTO login (username,mail,password,namedb) VALUES (%s,%s,%s,%s)',(username,email,password_hash,nameDB))
            conect.commit()
            #create user's db
            cursor.execute(f"CREATE TABLE {fusion}" 
                    "(id INT NOT NULL AUTO_INCREMENT,"
                    "name VARCHAR (255) NOT NULL,"
                    "amount INT (255) NOT NULL," 
                    "PRIMARY KEY (id));")
            flash("You're registed successfully",'alert-success')
            return redirect(url_for('user_register.loginup'))
        else:
            flash('Values ​​are missing!','alert-danger')
            return redirect(url_for('user_register.signup'))
    return render_template('signup.html')


@user_register.route('/loginup', methods=['GET','POST'])
def loginup():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['email'],request.form['password'])
        logged_user = ModelUser.login(conect,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                flash("You're logged in!",'alert-success')
                return redirect(url_for('baseControl.WorkerRegistration'))
            else:
                flash('Invalid Password!','alert-danger')
        else:
            flash('User not found!','alert-danger')
            
    return render_template('loginup.html')

@user_register.route('/logout')
def logout():
    logout_user()
    flash("'You're logged out'",'alert-info')
    return redirect(url_for('user_register.index'))