from client import MySQL
from metrics import *

def mysql_connections_handler(par):
    mysqlcli = MySQL(user=par["monitor_user"], password=par["monitor_password"])
    users = mysqlcli.get_users()
    mysql_user_num.set(len(users))
    user_connections = mysqlcli.get_user_connections()
    for user in users:
        if user not in user_connections.keys():
            mysql_connections.labels(user=user).set(0)
        else:
            mysql_connections.labels(user=user).set(user_connections[user])

def mysql_database_table_num_handler(par):
    mysqlcli = MySQL(user=par["monitor_user"], password=par["monitor_password"])
    contents = mysqlcli.query("show databases;")
    mysql_database_num.set(len(contents))
    databases = [info["Database"] for info in contents]
    for database in databases:
        contents = mysqlcli.query("select count(*) from information_schema.tables where table_schema='%s';" %database)
        mysql_table_num.labels(database=database).set(contents[0]["count(*)"])
