from rr import conf, db, html, mail
from datetime import datetime
import os


def get_file_name_plus_tod(file_name):
    file_base_name, file_ext = os.path.splitext(file_name)
    now = datetime.now()
    tod = now.strftime("%Y%m%d")
    new_file_name = file_base_name + '_' + tod + file_ext
    return new_file_name


if __name__ == '__main__':
    cfg = conf.AppConf()
    cfg.parse(conf.CONF_FILE_CANDIDATES)
    conn = db.DB(cfg)
    html = html.HTML()
    mailer = mail.Mail(cfg)

    backup_summary_list = conn.get_backup_summary()
    backup_detail_dict = conn.get_backup_details()
    msg_content = html.render(backup_summary_list, backup_detail_dict)
    mailer.add_attachment_from_string(get_file_name_plus_tod('backup_report.html'), msg_content)
    mailer.send(msg_content)
    print(msg_content)

