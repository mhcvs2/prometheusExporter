from prometheus_client import Gauge

mysql_connections = Gauge('mysql_connections', 'mysql user connections in using',["user"])
mysql_user_num = Gauge('mysql_user_num', 'mysql user numbers')
mysql_database_num = Gauge('mysql_database_num', 'mysql databases numbers')
mysql_table_num = Gauge('mysql_table_num', 'mysql databases numbers',["database"])
