from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import smtplib
import ssl

class modelSent():
    
    @classmethod
    def send(sefl, destinario):
        try:
            email = MIMEMultipart()
            sender = 'pablomorabarrantes@gmail.com'
            email['From'] = sender
            email['To'] = destinario
            email['Subject'] = 'Registro de cafe de la fecha {}.xlsx'.format(date.today()) 
            filename = f'Registro del dia {date.today()}.xlsx'
            attachment = open(filename, 'rb')
            attachment__package = MIMEBase('applitacion','octect-stream')
            attachment__package.set_payload((attachment).read())
            encoders.encode_base64(attachment__package)
            attachment__package.add_header('Content-Disposition','attachment; filename = '+filename)
            email.attach(attachment__package)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender,'zghacocmitefpkcv')
                smtp.sendmail(sender,destinario,email.as_string())
                smtp.quit()
                return email
            
        except Exception as ex:
            raise Exception(ex)



