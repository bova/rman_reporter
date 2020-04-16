import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import io

import rr.conf


class Mail:
    host = ''
    port = ''
    user = ''
    password = ''
    mail_from = ''
    mail_to = ''

    def __init__(self, cfg):
        self.cfg = rr.conf.AppConf()
        self.cfg = cfg
        self.host = self.cfg.mail.host
        self.port = self.cfg.mail.port
        self.user = self.cfg.mail.user
        self.password = self.cfg.mail.password
        self.mail_from = self.cfg.mail.mail_from
        self.mail_to = self.cfg.mail.mail_to

        self.msg = MIMEMultipart()
        # attachments: array of tuples (file_name, file)
        self.attachments = []
        context = ssl.create_default_context()
        self.mailer = smtplib.SMTP_SSL(host=self.host, port=self.port, context=context)

    def add_attachment_from_string(self, file_name, file_as_string):
        file = file_as_string.encode(encoding='utf-8')
        attachment = (file_name, file)
        self.attachments.append(attachment)

    def attach_files_to_message(self):
        for file_name, file in self.attachments:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file_name}",
            )
            self.msg.attach(part)

    def connect(self):
        if self.cfg.mail.user and self.cfg.mail.password:
            self.mailer.login(self.user, self.password)
        else:
            pass

    def create_msg(self, content):
        self.msg['From'] = self.mail_from
        self.msg['To'] = self.mail_to
        self.msg['Subject'] = "Test rman_reporter"
        self.msg.attach(MIMEText(content, 'html'))
        self.attach_files_to_message()
        return self.msg

    def send(self, content):
        self.connect()
        msg = self.create_msg(content)
        self.mailer.sendmail(self.mail_from, self.mail_to, msg.as_string())
        self.mailer.quit()
