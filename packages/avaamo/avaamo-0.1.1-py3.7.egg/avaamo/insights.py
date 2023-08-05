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

url = "https://{0}/dashboard/bot_domains/6996/test.json".format(ENDPOINT)

payload = "{\"text\":\"bob went to the zoo and mary went to the park\",\"language\":\"en\" }"
headers = {
    'Access-Token': ACCESS_TOKEN,
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(json.dumps(json.loads(response.text), separators=(', ', ': '), indent=4, sort_keys=True))
