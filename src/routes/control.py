from flask import Blueprint, render_template, flash, redirect, url_for, request
from Database.database import connect_base
from datetime import date
import os
from Models.modelSend import modelSend

conect = connect_base()
cursor =conect.cursor()


baseControl = Blueprint('baseControl',__name__,url_prefix='/base')



@baseControl.route('/',methods=['GET','POST'])
def calculator():
    sql = 'SELECT * FROM staff'
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('calculator.html', contacts = data)


@baseControl.route('/add_contact', methods=['GET','POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        cursor.execute('INSERT INTO staff (name,amount) VALUES (%s,%s)',(name,amount))
        conect.commit()
        flash('registration has been made','alert-success')
        return redirect(url_for('baseControl.calculator'))
    
    
    
    
@baseControl.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    cursor.execute('SELECT * FROM staff WHERE id={}'.format(id))
    data = cursor.fetchall()
    
    return render_template('edit.html', contact = data[0])




@baseControl.route('/update/<id>', methods=['GET','POST'])
def update(id):
    name = request.form['name']
    amount = request.form['amount']
    cursor.execute('UPDATE staff SET name=%s, amount=%s WHERE id=%s',(name,amount,id))
    conect.commit()
    flash('updated name','alert-success')
    return redirect(url_for('baseControl.calculator'))
    

@baseControl.route('/delete/<id>', methods=['GET','POST'])
def delete_u(id):
    cursor.execute('DELETE FROM staff WHERE id ={}'.format(id))
    flash('user deleted')
    conect.commit()
    return redirect(url_for('baseControl.calculator'))


#Elimina todos los datos de la base de datos (staff) 
@baseControl.route('/delete_all')
def delete_all():
    cursor.execute('DELETE FROM staff')
    conect.commit()
    return redirect(url_for('baseControl.calculator'))

@baseControl.route('/sent_data', methods = ['GET','POST'])
def sent_data():  
    if request.method == 'POST':
        sql = 'SELECT * FROM staff'
        cursor.execute(sql)
        data = cursor.fetchall()
        email_user = request.form['email_user']
        #create excel
        createecxel = modelSend.create_excel(data)
        #send the email
        if createecxel != None:   
            send_gmail = modelSend.send(email_user)
            if send_gmail != None:
                os.remove(f'Registro del dia {date.today()}.xlsx')
                flash('Sented','alert-success')
                return redirect(url_for('baseControl.delete_all'))
    return render_template('sent_data.html')