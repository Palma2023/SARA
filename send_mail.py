import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail(to_address, subject, body, attachment_path=None):
    from_address = "remi.brechemier@orange.fr"  # Votre adresse e-mail Orange
    password = ""  # Votre mot de passe Orange

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        filename = attachment_path.split('/')[-1]
        attachment = open(attachment_path, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)

    # Utiliser le serveur SMTP d'Orange
    server = smtplib.SMTP('smtp.orange.fr', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()
