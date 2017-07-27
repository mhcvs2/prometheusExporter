import os
import sys
import time
import logging as log
from collections import OrderedDict
from prometheus_client import start_http_server
from ConfigParser import ConfigParser
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%d %b %Y %H:%M:%S')

def main():
    if (len(sys.argv) < 2):
        log.error("Run with 'python %s configfile'" %sys.argv[0])
        sys.exit(1)
    configfile = sys.argv[1]
    if not os.path.isfile(configfile):
        log.error("%s is not a file." %configfile)
    if not os.path.exists(configfile):
        log.error("%s doesn't exist." %configfile)
    cnf = ConfigParser()
    cnf.read(configfile)
    port = cnf.getint("exporter","port")
    internal = cnf.getint("exporter", "internal")
    exporter = OrderedDict()

    for section in cnf.sections():
        if section == "exporter":
            continue
        par = {}
        options = cnf.options(section)
        for option in options:
            par[option] = cnf.get(section,option)
        metrics, handlers, handler_module = get(section)
        exporter[section] = {}
        exporter[section]["metrics"] = metrics
        exporter[section]["handlers"] = handlers
        exporter[section]["handler_module"] = handler_module
        exporter[section]["par"] = par

    run(port,internal,exporter)

def get(exporter_name):
    exporter_dir = exporter_name + "_exporter"
    handler_module = __import__(exporter_dir + ".handler", fromlist=[exporter_dir])
    metrics_module = __import__(exporter_dir + ".metrics", fromlist=[exporter_dir])
    metrics = [name for name in dir(metrics_module) if exporter_name + "_" in name]
    handlers = [name for name in dir(handler_module) if exporter_name + "_" in name and "_handler" in name]
    return metrics, handlers, handler_module

def run(port, internal, exporter):
    for name, info in exporter.items():
        message = ""
        message += "Monitoring %s: " %name
        for db_metric in info["metrics"]:
            message += db_metric + " "
        log.info(message)
    log.info("Internal: %s" % str(internal))
    log.info("Start http server, listen port %s" % port)
    start_http_server(port)

    try:
        while True:
            for name, info in exporter.items():
                for fun in info["handlers"]:
                    apply(getattr(info["handler_module"], fun),(info["par"],))
            time.sleep(internal)
    except KeyboardInterrupt:
        log.info("Exporter exit.")

if __name__ == '__main__':
    sys.exit(
        main()
    )
