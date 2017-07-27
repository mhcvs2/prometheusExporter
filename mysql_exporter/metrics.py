from prometheus_client import Gauge

mysql_connections = Gauge('mysql_connections', 'Description of gauge',["user"])