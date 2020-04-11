import configparser
from rr.const import CONF_FILE_CANDIDATES


class DB:
    """Database configuration
    """
    host = ''
    port = ''
    service_name = ''
    user = ''
    password = ''


class Mail:
    """Email configuration
    """
    host = ''
    port = ''
    user = ''
    password = ''
    mail_from = ''
    mail_to = ''


class AppConf:
    def __init__(self):
        self.db = DB()
        self.mail = Mail()
        self.run_cfg = configparser.ConfigParser()

    def init_db_cfg(self):
        self.db.host = self.run_cfg.get('db', 'host')
        self.db.port = self.run_cfg.get('db', 'port')
        self.db.service_name = self.run_cfg.get('db', 'service_name')
        self.db.user = self.run_cfg.get('db', 'user')
        self.db.password = self.run_cfg.get('db', 'password')

    def init_mail_cfg(self):
        self.mail.host = self.run_cfg.get('mail', 'host')
        self.mail.port = self.run_cfg.get('mail', 'port')
        self.mail.user = self.run_cfg.get('mail', 'user')
        self.mail.password = self.run_cfg.get('mail', 'password')
        self.mail.mail_from = self.run_cfg.get('mail', 'mail_from')
        self.mail.mail_to = self.run_cfg.get('mail', 'mail_to')

    def parse(self, conf_file):
        self.run_cfg.read(conf_file)

        self.init_db_cfg()
        self.init_mail_cfg()

if __name__ == "__main__":
    conf = AppConf()
    conf.parse(CONF_FILE_CANDIDATES)
    print(conf.db)
    print(conf.mail)
