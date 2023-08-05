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

import argparse
import json

from avaamo import CLI
from avaamo import API


class ConversationDump(CLI):

    def __init__(self):
        super(ConversationDump, self).__init__()
        self._config_path = None
        self._conversation_id = None
        self._page = None
        self._per_page = None

    def get_description(self):
        return "Extract analytics conversation data"

    def add_arguments(self):
        super(ConversationDump, self).add_arguments()

        self.parser.add_argument('-i', '--conversation_id', action='store', dest="conversation_id", required=True,
                                 help="Conversation Id")
        self.parser.add_argument('-p', '--page', action='store', dest="page", default="1", help="Page")
        self.parser.add_argument('-e', '--per_page', action='store', dest="per_page", default="1000",
                                 help="Results per page")

    def get_arguments(self):
        super(ConversationDump, self).get_arguments()

        self._conversation_id = self.args.conversation_id
        self._page = self.args.page
        self._per_page = self.args.per_page

    def run(self):
        self.handle_arguments()

        api = API(endpoint=self.endpoint, access_token=self.access_token)
        doc = api.get_conversation(conversation_id=self._conversation_id)
        print(json.dumps(json.loads(doc), sort_keys=True, indent=2, separators=(',', ': ')))

    def execute(self):
        self.handle_arguments()
        self.run()


def main():
    cli = ConversationDump()
    cli.execute()


if __name__ == '__main__':
    main()
