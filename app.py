from flask import Flask, render_template, request, session, g, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from models.modelUser import ModelUser
from models.modelSend import modelSent
from models.entities.user import User
from flask_login import LoginManager , login_user, logout_user, login_required



app = Flask(__name__)
mysql = MySQL(app)
login_manager_app = LoginManager(app)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flask_login'




app.secret_key= 'password'

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql,id)

@app.before_request
def before_resquest():
    if 'username' in session:
        g.user = session['username']
    else:
        g.user = None


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if not g.user:
        if request.method == 'POST':
            username = request.form['username']
            mail = request.form['mail']
            password = request.form['password']
            password_hash = generate_password_hash(password, 'sha256')
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO login (username,mail,password) VALUES (%s,%s,%s)',(username,mail,password_hash))
            mysql.connection.commit()
            cur.close()
            flash("You,ve registed successfully", "alert-success")
            
            return redirect(url_for('loginup'))
        
        return render_template('signup.html')
    
    flash("You're alredy logged in", "alert-primary")
    return redirect(url_for('index'))
            
    

@app.route('/loginup', methods=['GET','POST'])
def loginup():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['mail'],request.form['password'])
        logged_user = ModelUser.login(mysql,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                print(login_user(logged_user))
                flash("You're logged in")
                return redirect(url_for('calculator')) 
            else:
                flash('Invalid password')
                return render_template('loginup.html')
        else:
            flash('User not found')
            return render_template('loginup.html')
    else:
        return render_template('loginup.html') 
  
    
@app.route('/logout')
def logout():
    logout_user()
    flash("'You're logged out'")
    return redirect(url_for('index'))
          
                        
                        
@app.route('/add_contact', methods=['GET','POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO staff (name,amount) VALUES (%s,%s)',(name,amount))
        mysql.connection.commit()
        flash('registration has been made')
        return redirect(url_for('calculator'))
    
    
    
    
@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM staff WHERE id={}'.format(id))
    data = cur.fetchall()
    cur.close()
    
    return render_template('edit.html', contact = data[0])




@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    name = request.form['name']
    amount = request.form['amount']
    cur = mysql.connection.cursor()
    cur.execute('UPDATE staff SET name=%s, amount=%s WHERE id=%s',(name,amount,id))
    mysql.connection.commit()
    flash('updated name')
    return redirect(url_for('calculator'))
    

@app.route('/delete/<id>', methods=['GET','POST'])
def delete_u(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM staff WHERE id ={}'.format(id))
    flash('user deleted')
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calculator'))


#Elimina todos los datos de la base de datos (staff) 
@app.route('/delete_all')
def delete_all():
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM staff')
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calculator'))



@app.route('/sent_data', methods = ['GET','POST'])
def sent_data():  
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        sql = 'SELECT * FROM staff'
        cur.execute(sql)
        data = cur.fetchall()
        email_user = request.form['email_user']
        message = []
        for contact in data:
            i = '{},{}'.format(contact[1],contact[2])
            message.append(i)
        send_gmail = modelSent.send(email_user,str(message))
        if send_gmail != None:
            flash('Sented')
            return redirect('calculator')
    return render_template('sent_data.html')



    
@app.route('/calculator',methods=['GET','POST'])
def calculator():
    cur = mysql.connection.cursor()
    sql = 'SELECT * FROM staff'
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    return render_template('calculator.html', contacts = data)
    
    



with app.app_context():
    if __name__=='__main__':
        app.run(debug=True)