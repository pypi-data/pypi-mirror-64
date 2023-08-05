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
import requests
import json


class Messages(object):

    def __init__(self, end_point):
        self._end_point = end_point

    def send_message(self):
        template_path = "https://{0}/bots_api/v1/messages.json"
        end_point_url = template_path.format(self._end_point)
        logger.info("name: '{0}' url: '{1}'".format(name, url))
        document = {
            "document": {
                "language_id": 1,  # English
                "url": url,
                "name": name,
                "type": 'url'
            }
        }
        payload = json.dumps(document)
        logger.debug(payload)
        headers = {
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,ru;q=0.8",
            'content-type': "application/json;charset=UTF-8",
            'accept': "application/json",
            'Access-Token': self._access_token
        }
        logger.debug(headers)
        response = None
        try:
            response = requests.request("POST", end_point_url, data=payload, headers=headers)
            response.raise_for_status()
            logger.info(response)
        except Exception as e:
            logger.exception(e)

        return response