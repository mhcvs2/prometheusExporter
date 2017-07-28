from prometheus_client import Gauge

common_system_mem_total = Gauge('system_mem_total', 'system_mem_total')
common_system_mem_free = Gauge('system_mem_free', 'system_mem_free')
common_system_mem_buffers = Gauge('system_mem_buffers', 'system_mem_buffers')
common_system_mem_cache = Gauge('system_mem_cache', 'system_mem_cache')
common_system_mem_used = Gauge('system_mem_used', 'system_mem_used')

common_system_cpu_used_rate = Gauge('system_cpu_used_rate', 'system_cpu_used_rate')

common_system_disk_available = Gauge('system_disk_available', 'system_disk_available')
common_system_disk_capacity = Gauge('system_disk_capacity', 'system_disk_capacity')
common_system_disk_free= Gauge('system_disk_free', 'system_disk_free')