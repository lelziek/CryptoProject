import os
import re
import glob
import Utils.settings
from Utils.cent_logger import setup_root_logger


excluded_fixtures = []
pytest_plugins = []
# import all fixtures automatically, except for those being excluded.
glob_pattern = 'Fixtures' + os.sep + '**' + os.sep + '*.py'
for filename in glob.iglob(glob_pattern, recursive=True):

    is_init = re.search('__init__', filename)

    if is_init is None:
        is_excluded = False
        for excluded_fixture in excluded_fixtures:
            if re.search(excluded_fixture, filename):
                is_excluded = True

        if is_excluded is False:
            plugin_notation = re.sub(re.escape(".py"), '', filename)
            plugin_notation = re.sub(re.escape(os.sep), '.', plugin_notation)
            pytest_plugins.append(plugin_notation)


def pytest_addoption(parser):
    parser.addoption("--log_level", action="store", default="DEBUG", help="Set default logging level")
    parser.addoption("--log_dir", action="store", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Logs'), help="Set logging directory")
    parser.addoption("--log_config_file", action="store", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Utils', 'cent_logger.json'), help="log configuration file in json format")
    print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Utils', 'cent_logger.json'))


def pytest_configure(config):
    setup_root_logger(config.getoption('--log_level'), config.getoption('--log_dir'),
                      config.getoption('--log_config_file'))
