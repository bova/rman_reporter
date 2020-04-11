import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import rr.conf


class Mail:
    host = ''
    port = ''
    user = ''
    password = ''
    msg_from = ''
    msg_to = ''

    def __init__(self, cfg):
        self.cfg = rr.conf.AppConf()
        self.cfg = cfg
        self.host = self.cfg.mail.host
        self.port = self.cfg.mail.port
        self.user = self.cfg.mail.user
        self.password = self.cfg.mail.password
        self.mail_from = self.cfg.mail.mail_from
        self.mail_to = self.cfg.mail.mail_to
        context = ssl.create_default_context()
        self.mailer = smtplib.SMTP_SSL(host=self.host, port=self.port, context=context)

    def connect(self):
        self.mailer.login(self.user, self.password)

    def create_msg(self, content):
        msg = MIMEMultipart()
        msg['From'] = self.mail_from
        msg['To'] = self.mail_to
        msg['Subject'] = "Test rman_reporter"
        msg.attach(MIMEText(content, 'html'))
        return msg

    def send(self, content):
        self.connect()
        msg = self.create_msg(content)
        self.mailer.sendmail("@gmail.com", "@gmail.com", msg.as_string())
        self.mailer.quit()
