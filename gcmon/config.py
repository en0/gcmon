import yaml
from os import environ
from os.path import exists
from typing import List, Union

from gcmon.types import ConfigurationInterface


class Configuration(ConfigurationInterface):
    def __init__(self, source: dict):
        self.__source = source

    def get(self, key: str) -> any:
        root = self.__source
        for k in key.split(":"):
            if k in root:
                root = root[k]
            else:
                return None
        return root

    def get_section(self, key: str) -> ConfigurationInterface:
        val = self.get(key)
        if isinstance(val, dict):
            return Configuration(val)
        return None


class ConfigurationLoader:
    environment_key = "GCMON_CONFIG_PATH"
    default_paths = [
        "./gcmon.yaml",
        "~/.config/gcmon/gcmon.yaml",
        "/etc/gcmon/gcmon.yaml",
    ]

    def __init__(self, path: str = None):
        self.__path = path

    def load(self) -> ConfigurationInterface:
        path = self.__get_usable_path()
        with open(path, "r") as fd:
            source = yaml.load(fd, Loader=yaml.SafeLoader)
            return Configuration(source)

    def __get_usable_path(self) -> str:
        try:
            return next(p for p in self.__get_paths() if exists(p))
        except StopIteration:
            raise RuntimeError("Configuration Error: Unable to find configuration file.")

    def __get_paths(self) -> List[str]:
        if self.__path is not None:
            return [ self.__path ]
        elif ConfigurationLoader.environment_key in environ:
            return [ environ.get(ConfigurationLoader.environment_key) ]
        else:
            return ConfigurationLoader.default_paths


