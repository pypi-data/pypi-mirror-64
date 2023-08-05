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

from avaamo import Configuration
import argparse
import os


class CLI(object):

    def __init__(self):
        self.args = None
        self.bot_id = None
        self.access_token = None
        self.endpoint = None
        self.parser = None

    def get_description(self):
        """
        Returns a description of what this CLI performs
        :return:
        """
        return "Base CLI"

    def load_configuration(self, path):
        config = Configuration(path)
        config.load()
        return config

    def load_environment(self, path):
        self.bot_id = os.environ['AVAAMO_BOT_ID']
        self.access_token = os.environ['AVAAMO_ACCESS_TOKEN']

    def handle_arguments(self):
        """
        Abstract method for getting the command line arguments

        :return: None
        """
        self.parser = argparse.ArgumentParser(description=self.get_description())
        self.add_default_arguments()
        self.add_arguments()
        self.args = self.parser.parse_args()
        self.get_arguments()

    def add_default_arguments(self):
        """
        Standard argument for inputting the Access Token to authorize to the Avaamo APIs
        Assumes that an ArgumentParser() has been previously allocated.

        :return: None
        """
        self.parser.add_argument('-a', '--access-token', action='store', dest='access_token',
                                 metavar='access_token', required=False, help='API access token')
        self.parser.add_argument('-e', '--endpoint', action='store', dest='endpoint', metavar='endpoint',
                                 required=False, help='API endpoint or domain name')

    def add_arguments(self):
        """
        Add standard arguments to the CLI which is currently:

        Access Token
        Endpoint

        Child classes of CLI need to call this first in their own implementation

        :return: None
        """

    def get_arguments(self):
        """
        Fetch values from standard arguments.
        Assumes that the arguments have been parsed already
        :return: None
        """
        self.access_token = self.args.access_token
        self.endpoint = self.args.endpoint

    def initialize(self):
        """
        Performs the standard house keeping of the CLI:
            Handling of the default arguments
            Handling of the specific arguments of children CLI classes

        :return: None
        """
        self.handle_arguments()

    def execute(self):
        """
        To be implemented by child classes
        :return: None
        """
        pass
