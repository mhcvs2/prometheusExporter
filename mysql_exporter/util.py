from client import MySQL

def get_mysqlcli(par):
    if "port" in par.keys() and "host" in par.keys():
        mysqlcli = MySQL(user=par["monitor_user"], password=par["monitor_password"],port=par["port"],host=par["host"])
    else:
        mysqlcli = MySQL(user=par["monitor_user"], password=par["monitor_password"])
    return mysqlcli

def get_bool_value(value):
    if value.lower() in ["no","false"]:
        return 0
    else:
        return 1
