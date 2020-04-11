/* 
RMAN Reporter

RR_Rman_Backup_Job_Details
*/
create or replace view RR_Rman_Backup_Job_Details as
select Jd.Session_Key,
       Jd.Db_Name,
       jd.start_time,
       jd.end_time,
       Round(Elapsed_Seconds / 3600, 1) Hrs,
       Round(Jd.Input_Bytes / (1024 * 1024 * 1024), 1) Input_Gb,
       Round(Jd.Output_Bytes / (1024 * 1024 * 1024), 1) Output_Gb,
       Jd.Input_Type,
       Dd.Incremental_Level Incr_Lv,
       Jd.Output_Device_Type,
       Status
  from Rc_Rman_Backup_Job_Details Jd
  left outer join (select distinct Session_Key, Incremental_Level
                     from Rc_Backup_Datafile_Details) Dd
    on Jd.Session_Key = Dd.Session_Key
 order by Jd.Db_Name, Start_Time;
