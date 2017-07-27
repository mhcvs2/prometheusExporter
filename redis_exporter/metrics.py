from prometheus_client import Gauge

redis_connections = Gauge('redis_connections', 'Description of gauge')

redis_database_number = Gauge('redis_database_number', 'Description of gauge')