from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import smtplib
import ssl

class modelSent():
    
    @classmethod
    def send(sefl, destinario,html):
        try:
            email = MIMEMultipart()
            sender = 'pablomorabarrantes@gmail.com'
            email['From'] = sender
            email['To'] = destinario
            email['Subject'] = 'Registro de cafe de la fecha {}'.format(date.today()) 
            email.attach(MIMEText(html,'html'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender,'zghacocmitefpkcv')
                smtp.sendmail(sender,destinario,email.as_string())
                smtp.quit()
                return email
            
        except Exception as ex:
            raise Exception(ex)



