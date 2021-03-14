import yaml
import csv
from pathlib import Path
from os import walk, sep, path
from collections import namedtuple
import re
import logging

logger = logging.getLogger("framework")

home_dir = Path().absolute()
conf_dir = str(home_dir) + sep + "Config" + sep
fixtures_dir = str(home_dir) + sep + "Config" + sep + "fixtures" + sep
environment_dir = str(home_dir) + sep + "Config" + sep + "environment" + sep
tests_dir = str(home_dir) + sep + "Config" + sep + "tests" + sep


class Configs:
    """
    Includes static methods for the following:

    * Returning the home dir path from where the test are running
    * Returning a single YAML file as dictionary
    * Returning a single node of config data based on a filename and yaml node name
    * Returning a namedtuple object based on a config file and yaml node name
      ``c = Configs().get_yaml_node_as_tuple('yaml_file_name', 'yaml_node')``

    """

    @staticmethod
    def _tuple_factory(yaml_file, node, directory=conf_dir):
        yaml_data = Configs.get_yaml_node(yaml_file, node, directory)
        return(namedtuple(yaml_file, yaml_data.keys()))(**yaml_data)

    @staticmethod
    def get_yaml_node_as_tuple(yaml_file, node, directory=conf_dir):
        """
        Returns the node as a namedtuple object

        ``x = Configs().get_yaml_node_as_tuple('selenium', 'chrome_windows_local')``
        ``x.binary``
        ``'chrome.exe'``

        :param str yaml_file: yaml file name - does an 'in' lookup so you can skip the .yaml
        :param str node: yaml node to retrieve
        :return: namedtuple object
        """
        try:
            config_tuple = Configs._tuple_factory(yaml_file, node, directory)
            return config_tuple
        except AttributeError as ae:
            return None

    @staticmethod
    def get_environment_node(yaml_file, node):
        """
        Returns a config node for an environment config file.
        ``x = Configs().get_environment_node('selenium', 'chrome_windows_local')``
        ``x.binary``
        ``'chrome.exe'``

        :param str yaml_file: yaml file name of a config in the environment sub directory - does an 'in' lookup so you can skip the .yaml
        :param str node: yaml node to retrieve
        :return: namedtuple object
        """
        return Configs.get_yaml_node_as_tuple(yaml_file, node, environment_dir)._asdict()

    @staticmethod
    def get_fixture_node(yaml_file, node):
        """
        Returns a config node for an fixture config file.
        ``x = Configs().get_fixture_node('selenium', 'chrome_windows_local')``
        ``x.binary``
        ``'chrome.exe'``

        :param str yaml_file: yaml file name of a config in the fixtures sub directory - does an 'in' lookup so you can skip the .yaml
        :param str node: yaml node to retrieve
        :return: namedtuple object
        """
        return Configs.get_yaml_node_as_tuple(yaml_file, node, fixtures_dir)._asdict()

    @staticmethod
    def get_test_node(yaml_file, node):
        """
        Returns a config node for a test config file.
        ``x = Configs().get_fixture_node('selenium', 'chrome_windows_local')``
        ``x.binary``
        ``'chrome.exe'``

        :param str yaml_file: yaml file name of a config in the tests sub directory - does an 'in' lookup so you can skip the .yaml
        :param str node: yaml node to retrieve
        :return: namedtuple object
        """
        return Configs.get_yaml_node_as_tuple(yaml_file, node, tests_dir)._asdict()

    @staticmethod
    def get_fs_home_dir():
        return str(home_dir.parent.parent)

    @staticmethod
    def get_node(yaml_file, node):
        """
        Returns a config node for a test config file.
        ``x = Configs().get_fixture_node('selenium', 'chrome_windows_local')``
        ``x.binary``
        ``'chrome.exe'``

        :param str yaml_file: yaml file name of a config in the tests sub directory - does an 'in' lookup so you can skip the .yaml
        :param str node: yaml node to retrieve
        :return: namedtuple object
        """
        return Configs.get_yaml_node_as_tuple(yaml_file, node)._asdict()

    @staticmethod
    def get_yaml_node(yaml_name, node, directory=conf_dir):
        """
        returns a top level node, by name, from the specified yaml config file

        :param str yaml_name: name of the yaml file - appends the .yaml in lookup, so you can skip the .yaml
        :param str node: name of the config node inside the YAML file you specified
        :return: yaml node as dictionary
        """

        yaml_list = []
        print(directory)
        for root, _, files in walk(directory):
            for filename in files:
                if filename != "local.yaml":
                    file_path = str(Path(root + sep + filename))
                    yaml_list.append(file_path)
        print(yaml_list)
        for i in yaml_list:
            base_dir, file_name = path.split(i)
            if file_name == yaml_name + ".yaml":
                with open(i) as f:
                    yaml_data = f.read()
                    yaml_search = yaml.load(yaml_data, Loader=yaml.FullLoader)
                    for _ in yaml_search[yaml_name]:
                        if _ == node:
                            yaml_return = yaml_search[yaml_name][_]
                            return yaml_return

    @staticmethod
    def get_parametrized_yaml_node_names(yaml_name, pattern, strict=True):
        """
        returns a namedtuple consisting of a list of yaml nodes and a list of those node's names

        :param str yaml_name: name of the yaml file - does an 'in' lookup, so you can skip the .yaml
        :param str pattern: string to match against.  When in strict mode, this string will be matched completely.
        :param bool strict: enable strict mode. Matches the exact string
        :return: yaml as dictionary
        """

        needle = "^"+re.escape(pattern)+"$"
        logger.debug(f"yaml_name is {yaml_name}")
        logger.debug(f"needle is {needle}")
        logger.debug(f"Strict mode enabled: {strict}")

        id_list = []
        comp = re.compile(needle, re.IGNORECASE)

        yaml_list = []
        for _, _, files in walk(conf_dir):
            for filename in files:
                if filename != "local.yaml":
                    yaml_list.append(filename)
                if strict:
                    yaml_list = [yaml_name + ".yaml"]

        for i in yaml_list:
            if yaml_name in i:
                with open(conf_dir + i) as f:
                    yaml_data = f.read()
                    yaml_search = yaml.load(yaml_data, Loader=yaml.FullLoader)
                    for _ in yaml_search[yaml_name]:
                        if comp.search(_) is not None:
                            id_list.append(_)
        return id_list
