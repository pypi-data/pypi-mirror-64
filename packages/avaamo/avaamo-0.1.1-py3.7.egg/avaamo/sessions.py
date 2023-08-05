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

import os
import requests
import json
from pprint import pprint

ENDPOINT = os.environ['AVAAMO_ENDPOINT']
ACCESS_TOKEN = os.environ['AVAAMO_ACCESS_TOKEN']
BOT_ID = os.environ['AVAAMO_BOT_ID']


url = "https://c0.avaamo.com/bots_api/v1/analytics/{0}/sessions.json".format(BOT_ID)

querystring = {
    "from_date": "12/01/2017",
    "to_date": "3/31/2019",
    "per_page": 100,
    "page": 1
}

payload = ""
headers = {
    'Access-Token': ACCESS_TOKEN,
    'Content-Type': "application/json",
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(json.dumps(json.loads(response.text), separators=(', ', ': '), indent=4, sort_keys=True))
