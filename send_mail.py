# SendMail.py

import smtplib, datetime, os, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#working with orange but not with gmail because problem of security. 
#If we want to search how to activate connection from less security application

USERNAME = 'remi.brechemier@orange.fr'  # Username for authentication
PASSWORD = ''  # Password for authentication
SMTP_SERVER = 'smtp.orange.fr'  # URL of SMTP server

FROM = "remi.brechemier@orange.fr"  # Name shown as sender
TO = 'thomas.chauchot@groupe-esigelec.org' # Mail address of the recipient
SSL_PORT = 465

def sendMail(subject, text, img = None):
    print("Sending the mail...")
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(text, "html"))
    
    tmpmsg = msg
    msg = MIMEMultipart()
    msg.attach(tmpmsg)
    if img != None:
        if not os.path.exists(img):
            print("File", img, "does not exist.") 
        else:
            fp = open(img, 'rb')
            img = MIMEImage(fp.read())  # included in mail, not as attachment
            fp.close()
            msg.attach(img)        
    
    msg['Subject'] = subject
    msg['From'] = FROM
    server = smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT)
    server.login(USERNAME, PASSWORD)
    server.sendmail(FROM, [TO], msg.as_string())
    server.quit()
    print("Mail successfully sent.")
