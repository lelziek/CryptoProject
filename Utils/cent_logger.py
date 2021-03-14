import os
import sys
import logging
import logging.config
import json


logger = logging.getLogger(__name__)


def setup_root_logger(loglevel=logging.DEBUG, logdir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Logs'),
                      log_config_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Utils', 'cent_logger.json')):
    """ Setup a root logger for this tests run """
    try:

        if not os.path.isdir(logdir):
            os.makedirs(logdir)

        if log_config_file is not None and os.path.exists(log_config_file):
            with open(log_config_file, 'rt') as logconf:
                config = json.load(logconf)
                # create absolute path for logfile
                config['handlers']['file_handler']['filename'] = logdir + '/' + config['handlers']['file_handler']['filename']
                config['handlers']['longterm']['filename'] = logdir + '/' + config['handlers']['longterm']['filename']
                config['handlers']['single_run']['filename'] = logdir + '/' + config['handlers']['single_run']['filename']
                root_logger = logging.getLogger("framework")
                logging.config.dictConfig(config)
                logger.info("I initialized the framework logger")
                root_logger.info("Configured basic root logger from: {}".format(log_config_file))
                test_logger = logging.getLogger("tests")
                logging.config.dictConfig(config)
                logger.info("I initialized the tests logger")
                test_logger.info("Configured basic tests logger from: {}".format(log_config_file))

                # disable logs from below external modules
                for disabled_module in config['disable_module_logs']:
                    root_logger.debug('Disabled logging for module: {}'.format(disabled_module))
                    logging.getLogger(disabled_module).disabled = True

    except Exception as e:
        print("Error configuring logger: {}".format(e), file=sys.stderr)
        raise e#


def get_trace_logger(name, logdir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Logs'), loglevel=logging.DEBUG):
    try:
        trace_logger = logging.getLogger(name)
        trace_log_dir = os.path.join(logdir, name)
        if not os.path.isdir(trace_log_dir):
            os.makedirs(trace_log_dir)

        # Create tests case log file handler
        log_formatter = logging.Formatter(
            "%(asctime)s_%(msecs)d: %(name)s: %(filename)s: %(lineno)s: %(levelname)s: %(message)s")
        rotating_handler = logging.handlers.RotatingFileHandler(os.path.join(trace_log_dir, "{}.log".format(name)),
                                                                mode='a', maxBytes=10485760, backupCount=20, encoding=None,
                                                                delay=0)
        rotating_handler.setLevel(loglevel)
        rotating_handler.setFormatter(log_formatter)
        trace_logger.addHandler(rotating_handler)
        trace_logger.info("Created tc logger for: {}".format(name))
        return trace_logger
    except Exception as e:
        logger.exception("Error configuring trace logger: {}".format(e))
        raise e

