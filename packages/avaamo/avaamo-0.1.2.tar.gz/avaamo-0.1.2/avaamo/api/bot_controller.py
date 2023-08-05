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
import os
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BotController(object):
    def __init__(self):
        try:
            self._access_token = os.environ['AVAAMO_ACCESS_TOKEN']
            self._end_point = os.environ['AVAAMO_END_POINT']
            self._connector_id = os.environ['AVAAMO_CONNECTOR_ID']
            self._channel_id = os.environ['AVAAMO_CHANNEL_ID']
            self._uuid = os.environ['AVAAMO_UUID']
            self._first_name = os.environ['AVAAMO_USER_FIRST_NAME']
            self._last_name = os.environ['AVAAMO_USER_LAST_NAME']
        except KeyError as e:
            logger.error(e)

    def call_message_api(self, text):
        url = "https://{0}/bot_connector_webhooks/{1}/message.json".format(self._end_point, self._connector_id)
        logger.debug(url)

        document = {
            "channel_uuid": self._channel_id,
            "user": {
                "first_name": self._first_name,
                "last_name": self._last_name,
                "uuid": self._uuid
            },
            "message": {
                "text": text
            }
        }
        payload = json.dumps(document)
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        logger.debug(headers)
        logger.debug(payload)
        response = None
        try:
            response = requests.request("POST", url=url, data=payload, headers=headers)
        except Exception as e:
            logger.exception(e)

        return response

    def send_message(self, message):
        """
        :return: Dictionary of the response from the virtual assistant
        """
        logger.debug(message)
        response = self.call_message_api(message)
        logger.debug(response)
        return response.json()
