from util import *
from metrics import *

def mysql_exporter_handler(par):
    mysqlcli = get_mysqlcli(par)
    get_connections(mysqlcli)
    get_database_table_num(mysqlcli)
    get_slave_status(mysqlcli)
    get_master_status(mysqlcli)

def get_connections(mysqlcli):
    users = mysqlcli.get_users()
    mysql_user_num.set(len(users))
    user_connections = mysqlcli.get_user_connections()
    for user in users:
        if user not in user_connections.keys():
            mysql_connections.labels(user=user).set(0)
        else:
            mysql_connections.labels(user=user).set(user_connections[user])

def get_database_table_num(mysqlcli):
    contents = mysqlcli.query("show databases;")
    mysql_database_num.set(len(contents))
    databases = [info["Database"] for info in contents]
    for database in databases:
        contents = mysqlcli.query("select count(*) from information_schema.tables where table_schema='%s';" %database)
        mysql_table_num.labels(database=database).set(contents[0]["count(*)"])

def get_slave_status(mysqlcli):
    master_info_key = ["Master_Host","Master_User","Master_Port","Master_Server_Id","Master_UUID"]
    log_file_key = ["Master_Log_File","Relay_Log_File","Relay_Master_Log_File"]
    bool_key = ["Master_SSL_Verify_Server_Cert","Master_SSL_Allowed","Slave_IO_Running","Slave_SQL_Running"]
    common_key = ["Connect_Retry","Read_Master_Log_Pos","Relay_Log_Pos","Last_Errno","Skip_Counter","Exec_Master_Log_Pos",
                  "Relay_Log_Space","Seconds_Behind_Master","Last_IO_Errno","Last_SQL_Errno","SQL_Delay","Master_Retry_Count","Auto_Position"]
    contents = mysqlcli.query("show slave status;")
    if len(contents) == 0:
        slave_status = {}
        for k in master_info_key:
            slave_status[k] = "null"
        for k in log_file_key:
            slave_status[k] = "null"
        for k in bool_key:
            slave_status[k] = "No"
        for k in common_key:
            slave_status[k] = 0
        slave = 0
    else:
        slave_status = contents[0]
        slave = 1


    mysql_slave_status_master_info.labels(Master_Host = slave_status["Master_Host"],
                                          Master_User = slave_status["Master_User"],
                                          Master_Port = slave_status["Master_Port"],
                                          Master_Server_Id = slave_status["Master_Server_Id"],
                                          Master_UUID = slave_status["Master_UUID"]).set(slave)
    mysql_slave_status_log_file.labels(Master_Log_File = slave_status["Master_Log_File"],
                                       Relay_Log_File = slave_status["Relay_Log_File"],
                                       Relay_Master_Log_File = slave_status["Relay_Master_Log_File"]).set(slave)
    for k in bool_key:
        mysql_slave_status.labels(name=k).set(get_bool_value(slave_status[k]))
    for k in common_key:
        mysql_slave_status.labels(name=k).set(slave_status[k])

def get_master_status(mysqlcli):
    common_key = ["File","Position"]
    contents = mysqlcli.query("show master status;")
    if len(contents) == 0:
        master_status = {}
        for k in common_key:
            master_status[k] = "null"
        master = 0
    else:
        master_status = contents[0]
        master = 1
    mysql_master_status.labels(File = master_status["File"],
                               Position = master_status["Position"]).set(master)

