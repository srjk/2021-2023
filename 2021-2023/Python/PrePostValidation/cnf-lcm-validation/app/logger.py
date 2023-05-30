import logging
from datetime import datetime
from datetime import date
from time import strftime
from time import sleep

def init_logging():

        today=datetime.now()
        date_time = today.strftime("%m-%d-%Y-%H:%M:%S:%f")

        logfile = "Test-logs-"+date_time+".log"
        kibana_logfile = "kibana-logs-"+date_time+".log"
        error_logfile = "error-logs-"+date_time+".log"



        logging.getLogger('').setLevel(logging.DEBUG)
        def create_log_file(filename, level=logging.INFO):
            handler = logging.FileHandler(filename)
            handler.setLevel(level)

            #request ID must be added
            formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logging.getLogger('').addHandler(handler)

        create_log_file(kibana_logfile, logging.INFO)
        #create_log_file(logfile, logging.INFO)
        create_log_file(error_logfile, logging.ERROR)

        # Now, we can log to the root logger, or any other logger. First the root...
        #logging.info('Jackdaws love my big sphinx of quartz.')

        # Now, define a couple of other loggers which might represent areas in application:

        logger_cluster= logging.getLogger('cluster_login')
        logger_show = logging.getLogger('show_commands')
        logger_error = logging.getLogger()

        return logger_cluster


        # logger_cluster.debug('Quick zephyrs blow, vexing daft Jim.')
        # logger_show.info('How quickly daft jumping zebras vex.')
        # logger_show.error('error How quickly daft jumping zebras vex.')
        # logger_cluster.warning('Jail zesty vixen who grabbed pay from quack.')
        # logger_error.error('The five boxing wizards jump quickly.')

