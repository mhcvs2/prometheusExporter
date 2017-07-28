from metrics import *
import time

def common_mem_handler(par):
    with open('/proc/meminfo') as f:
        total = int(f.readline().split()[1])
        free = int(f.readline().split()[1])
        buffers = int(f.readline().split()[1])
        cache = int(f.readline().split()[1])
        used = total - free - buffers - cache

    common_system_mem_total.set(total*1024)
    common_system_mem_free.set(free*1024)
    common_system_mem_buffers.set(buffers*1024)
    common_system_mem_cache.set(cache*1024)
    common_system_mem_used.set(used*1024)

def _read_cpu_usage():
    fd = None
    try:
        fd = open("/proc/stat", 'r')
        lines = fd.readlines()
    finally:
        if fd:
            fd.close()
    for line in lines:
        l = line.split()
        if len(l) < 5:
            continue
        if l[0].startswith('cpu'):
            return l
    return []

def common_cpu_handler(par):
    """ 
    get cpu avg used by percent 
    """
    cpustr = _read_cpu_usage()
    if not cpustr:
        return 0
    # cpu usage=[(user_2 +sys_2+nice_2) - (user_1 + sys_1+nice_1)]/(total_2 - total_1)*100
    # www.iplaypy.com
    usni1 = long(cpustr[1]) + long(cpustr[2]) + long(cpustr[3]) + long(cpustr[5])+long(cpustr[6]) + long(cpustr[7]) + long(cpustr[4])
    usn1 = long(cpustr[1]) + long(cpustr[2]) + long(cpustr[3])
    time.sleep(2)
    cpustr = _read_cpu_usage()
    if not cpustr:
        return 0
    usni2 = long(cpustr[1]) + long(cpustr[2]) + float(cpustr[3]) + long(cpustr[5])+long(cpustr[6]) + long(cpustr[7]) + long(cpustr[4])
    usn2 = long(cpustr[1]) + long(cpustr[2]) + long(cpustr[3])
    cpuper = (usn2 - usn1) / (usni2 - usni1)
    common_system_cpu_used_rate.set("%2f" %float(cpuper*100))


def common_disk_handler(par):
    import os
    disk = os.statvfs("/")
    available = disk.f_bsize * disk.f_bavail
    capacity = disk.f_bsize * disk.f_blocks
    free = disk.f_bsize * disk.f_bfree
    common_system_disk_available.set(available)
    common_system_disk_capacity.set(capacity)
    common_system_disk_free.set(free)
