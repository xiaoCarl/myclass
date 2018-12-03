import ConfigParser
import logging


def log_level_get(level):
    DEBUG_LEVEL={'CRITICAL':logging.CRITICAL,'ERROR':logging.ERROR,'WARNING':logging.WARNING,
                 'INFO':logging.INFO,'DEBUG':logging.DEBUG }
    return DEBUG_LEVEL.get(level.upper())


def log_config(config_file):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)

    config_log_level = cf.get("log", "level")
    config_log_file  = cf.get("log", "log_file")

    log_level = log_level_get(config_log_level)


    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename = config_log_file, 
                        level=log_level,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)



log_config("my.conf")
logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")
logging.warning('%s is %d years old.', 'Tom', 10)
