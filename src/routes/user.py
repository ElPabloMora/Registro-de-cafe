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
        password_hash = generate_password_hash(password,'sha256')
        cursor.execute('INSERT INTO login (username,mail,password) VALUES (%s,%s,%s)',(username,email,password_hash))
        conect.commit()
        flash("You're registed successfully",'alert-success')
        
        return redirect(url_for('user_register.loginup'))
    
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
                return redirect(url_for('baseControl.calculator'))
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