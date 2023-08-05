#   Copyright 2019 Avaamo, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import sys
import csv
import logging
from urllib.parse import urlparse
from avaamo import CLI
from avaamo import Answers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ListDocuments(CLI):
    """
    This command line tool can be used to lists the documents in a Avaamo Answers knowledge pack.
    """

    def __init__(self):
        super(CLI, self).__init__()
        self._answers = Answers()
        self._kp_id = None

    def get_description(self):
        """
        :return: Description of the CLI
        """
        return "Lists the URLs in an Avaamo Answers knowledge pack"

    def add_arguments(self):
        self.parser.add_argument('-k', '--knowledge-pack-id', action='store', dest='kp_id',
                                 metavar='id', required=True, help="Id of the knowledge pack to add the document")
        self.parser.add_argument('-d', '--debug', action='store_true', dest='debug', required=False,
                                 help="sets the logging")

    def get_arguments(self):
        """
        Extract the command line arguments from the Namespace provide by argparse

        :return: None
        """
        logger.debug(self.args)
        self._kp_id = self.args.kp_id

    def list_documents(self):
        """
        :return: None
        """
        response = self._answers.list_document(self._kp_id)
        document = response.json()
        writer = csv.DictWriter(sys.stdout, fieldnames=['url', 'name'], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for kd in document['knowledge_documents']:
            writer.writerow({"url": kd['url'], "name": kd['name']})

    def execute(self):
        self.initialize()
        self.list_documents()

    def run(self):
        self.execute()


def main():
    cli = ListDocuments()
    cli.run()


if __name__ == '__main__':
    main()
