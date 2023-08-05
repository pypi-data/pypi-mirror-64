# Copyright 2019 Avaamo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from configparser import ConfigParser
import logging

logger = logging.getLogger(__name__)

CONFIGURATION_NAME = '.avaamo'


class Configuration(object):

    def __init__(self, path):
        self._configuration = None
        self._path = path
        logger.info("Reading configuration from: {0}".format(self._path))
        self._parser = ConfigParser()

    def load(self):
        self._parser.read(self._path)
        logger.info("Configuration file contains these sections: {0}".format(self._parser.sections()))

    def get(self, section, key):
        logger.info("Lookup value in section: {0}, key: {1}".format(section, key))
        return self._parser.get(section, key)

