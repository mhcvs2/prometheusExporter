from metrics import *

def redis_connections_handler(par):
    redis_connections.set("100")

def redis_database_number_handler(par):
    redis_database_number.set("100")
