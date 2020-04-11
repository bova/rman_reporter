from rr import conf, db, html, mail



if __name__ == '__main__':
    cfg = conf.AppConf()
    cfg.parse(conf.CONF_FILE_CANDIDATES)
    conn = db.DB(cfg)
    html = html.HTML()
    mailer = mail.Mail(cfg)

    backup_summary_list = conn.get_backup_summary()
    backup_detail_dict = conn.get_backup_details()
    msg_content = html.render(backup_summary_list, backup_detail_dict)
    mailer.send(msg_content)
    print(msg_content)

