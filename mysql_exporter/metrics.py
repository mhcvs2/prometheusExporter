from prometheus_client import Gauge

mysql_connections = Gauge('mysql_connections', 'mysql user connections in using',["user"])
mysql_user_num = Gauge('mysql_user_num', 'mysql user numbers')
mysql_database_num = Gauge('mysql_database_num', 'mysql databases numbers')
mysql_table_num = Gauge('mysql_table_num', 'mysql databases numbers',["database"])
mysql_slave_status_master_info = Gauge('mysql_slave_status_master_info',
                                       'master info in SHOW SLAVE STATUS;',
                                       ["Master_Host","Master_User","Master_Port","Master_Server_Id","Master_UUID"])
mysql_slave_status_log_file = Gauge('mysql_slave_status_log_file',
                                       'log file in SHOW SLAVE STATUS;',
                                       ["Master_Log_File","Relay_Log_File","Relay_Master_Log_File"])
mysql_slave_status = Gauge('mysql_slave_status',
                                       'values of SHOW SLAVE STATUS;',
                                       ["name"])

mysql_master_status = Gauge('mysql_master_status',
                                       'values of SHOW MASTER STATUS;',
                                       ["File","Position"])
