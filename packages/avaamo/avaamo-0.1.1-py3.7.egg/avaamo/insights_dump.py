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
from datetime import datetime

from avaamo import CLI
from avaamo import API


class InsightsDump(CLI):

    def __init__(self):
        """
        Initialize our InsightsDump class instance
        """
        super(InsightsDump, self).__init__()
        self.bot_id = None
        self.start_dt = None
        self.end_dt = None
        self.config_path = None

    def get_description(self):
        """
        InsightsDump specific description
        :return: Description of Insights Dump CLI
        """
        return "Extract analytics data"

    def add_arguments(self):
        super(InsightsDump, self).add_arguments()

        self.parser.add_argument('-b', '--bot-id', action='store', dest="bot_id", metavar='bot_id', required=True,
                                 help="Specifies the bot to export data from")
        self.parser.add_argument('-e', '--end-dt', action='store', dest="end_dt", metavar='YYYY-MM-DD', required=True,
                                 help="End Date")
        self.parser.add_argument('-s', '--start-dt', action='store', dest="start_dt", metavar='YYYY-MM-DD',
                                 required=True, help="Start Date")

    def get_arguments(self):
        super(InsightsDump, self).get_arguments()
        self.bot_id = self.args.bot_id
        self.start_dt = self.args.start_dt
        self.end_dt = self.args.end_dt

    def initialize(self):
        pass

    def run(self):
        api = API(endpoint=self.endpoint, access_token=self.access_token)

        dt_format = '%Y-%m-%d'
        start_dt = datetime.strptime(self.start_dt, dt_format)
        end_dt = datetime.strptime(self.end_dt, dt_format)

        # Make API call to get insights
        doc = api.result_by_filters(bot_id=self.bot_id, start_dt=start_dt, end_dt=end_dt)

        # Output JSON document
        print(json.dumps(json.loads(doc), sort_keys=True, indent=2, separators=(',', ': ')))

    def execute(self):
        self.initialize()
        self.handle_arguments()
        self.run()


def main():
    cli = InsightsDump()
    cli.execute()


if __name__ == '__main__':
    main()
