from client import MySQL
from metrics import *

def mysql_connections_handler(par):
    mysqlcli = MySQL(user=par["monitor_user"], password=par["monitor_password"])
    users = mysqlcli.get_users()
    user_connections = mysqlcli.get_user_connections()
    for user in users:
        if user not in user_connections.keys():
            mysql_connections.labels(user=user).set(0)
        else:
            mysql_connections.labels(user=user).set(user_connections[user])
