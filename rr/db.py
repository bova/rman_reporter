import cx_Oracle
import rr.conf

BACKUP_SUMMARY_SQL = """
select Db_Name,
       count(*) Backups,
       count(Case
               when Incr_Lv = 0 then
                1
             end) Incr_Lv0,
       count(Case
               when Incr_Lv = 1 then
                1
             end) Incr_Lv1,
       count(Case
               when Input_Type = 'RECVR AREA' then
                1
             end) Recvr_Area,
       COUNT(CASE
               WHEN Status in ('COMPLETED', 'COMPLETED WITH WARNINGS') THEN
                1
             END) Completed,
       COUNT(CASE
               WHEN Status in ('COMPLETED WITH ERRORS', 'FAILED') THEN
                1
             END) Failed,
       sum(Input_Bytes) Input_Bytes,
       sum(Output_Bytes) Output_Bytes
  from Rr_Rman_Backup_Job_Details
 where End_Time > Trunc(SYSDATE - 7)
 group by Db_Name"""

BACKUP_DETAILS_DB_NAMES_SQL = """
    select distinct Db_Name
      from Rr_Rman_Backup_Job_Details
     where End_Time > Trunc(SYSDATE-7)"""

BACKUP_DETAILS_SQL = """
    select Db_Name,
           Start_Time,
           End_Time,
           Hrs,
           input_bytes,
           output_bytes,
           Input_Type,
           Incr_Lv,
           Output_Device_Type,
           Status
      from Rr_Rman_Backup_Job_Details
     where End_Time > Trunc(SYSDATE - 7)
     order by Db_Name, Start_Time"""


class BackupSummary:
    db_name = ''
    backups = ''
    incr_lv0 = ''
    incr_lv1 = ''
    recvr_area = ''
    completed = ''
    failed = ''
    input_bytes = ''
    output_bytes = ''

    def __init__(self, cur_result):
        self.db_name = cur_result[0]
        self.backups = cur_result[1]
        self.incr_lv0 = cur_result[2]
        self.incr_lv1 = cur_result[3]
        self.recvr_area = cur_result[4]
        self.completed = cur_result[5]
        self.failed = cur_result[6]
        self.input_bytes = cur_result[7]
        self.output_bytes = cur_result[8]


class BackupDetail:
    db_name = ''
    start_time = ''
    end_time = ''
    hrs = ''
    input_bytes = ''
    output_bytes = ''
    input_type = ''
    incr_lv = ''
    output_device_type = ''
    status = ''

    def __init__(self, cur_result):
        self.db_name = cur_result[0]
        self.start_time = cur_result[1]
        self.end_time = cur_result[2]
        self.hrs = cur_result[3]
        self.input_bytes = cur_result[4]
        self.output_bytes = cur_result[5]
        self.input_type = cur_result[6]
        self.incr_lv = cur_result[7]
        self.output_device_type = cur_result[8]
        self.status = cur_result[9]


class BackupDetailsSerializer:
    def __init__(self, cur):
        self.cur = cur
        self.backup_details_dict = {}
    def get_db_names(self):
        for row in self.cur.execute(BACKUP_DETAILS_DB_NAMES_SQL):
            self.backup_details_dict[row[0]] = []
    def get_backup_details(self):
        for row in self.cur.execute(BACKUP_DETAILS_SQL):
            backup_detail = BackupDetail(row)
            list_for_row = self.backup_details_dict[backup_detail.db_name]
            list_for_row.append(backup_detail)

    def process(self):
        self.get_db_names()
        self.get_backup_details()
        return self.backup_details_dict



class DB:
    def __init__(self, cfg):
        self.cfg = rr.conf.AppConf()
        self.cfg = cfg
        self.conn_url = self.get_conn_url()
        self.conn = ''

    def get_conn_url(self):
        connection_url = self.cfg.db.host + ':' + self.cfg.db.port + '/' + self.cfg.db.service_name
        return connection_url

    def get_connection(self):
        self.conn = cx_Oracle.connect(self.cfg.db.user, self.cfg.db.password, self.conn_url)

    def execute_query(self):
        cur = self.conn.cursor()
        for row in cur.execute('select * from user_tables'):
            print(row)

    def get_backup_summary(self):
        backup_summary_list = []
        self.get_connection()
        cur = self.conn.cursor()
        for row in cur.execute(BACKUP_SUMMARY_SQL):
            backup_summary = BackupSummary(row)
            backup_summary_list.append(backup_summary)
        return backup_summary_list

    def get_backup_details(self):
        self.get_connection()
        cur = self.conn.cursor()
        backup_details = BackupDetailsSerializer(cur)
        return backup_details.process()



if __name__ == '__main__':
    conf = rr.conf.AppConf()
    conf.parse(rr.conf.CONF_FILE_CANDIDATES)
    conn = DB(conf)
    print(conn.get_backup_summary())
    print(conn.get_backup_details())