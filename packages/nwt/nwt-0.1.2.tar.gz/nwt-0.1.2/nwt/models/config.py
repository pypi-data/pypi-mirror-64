#! -*- coding: utf-8 -*-
"""
nwt.models.config
-----------------

Configuration of nwt.
"""
import toml
from logzero import logger as log

from . import HOME_DIR, touch
from ..controllers.error import ConfigError


class Config:
    def __init__(self, conf_file=None):
        self.conf_file = conf_file or HOME_DIR / 'config.toml'
        try:
            touch(self.conf_file, True)
            self.conf = toml.load(self.conf_file)
        except toml.decoder.TomlDecodeError as error:
            raise ConfigError(error)

    def save(self):
        log.debug("Saving config")
        with self.conf_file.open('w') as fd:
            toml.dump(self.conf, fd)

        self.conf = toml.load(self.conf_file)
        log.debug("config saved")

    def __getitem__(self, key):
        self.conf = toml.load(self.conf_file)
        try:
            return self.conf[key]
        except KeyError:
            log.debug(f"config [{key}] doesn't exists")
            return None

    def __setitem__(self, key, value):
        log.debug(f"set config [{key}] to '{value}'")
        self.conf[key] = value
        self.save()
