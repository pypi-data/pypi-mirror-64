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

import requests
import json
import logging


logger = logging.getLogger(__name__)

API_DATE_FORMAT = '%d/%m/%Y'


class API(object):

    def __init__(self, access_token, endpoint):
        """
        Instantiates an Avaamo API for calling public APIs

        :param access_token: Bearer token for API access
        :param endpoint: Instance of Avaamo to contact e.g. c0.avaamo.com
        """
        self._access_token = access_token
        self._endpoint = endpoint

    def result_by_filters(self, bot_id, start_dt, end_dt, utc_offset=0, page=1, per_page=100):
        """
        Provides a complete output of intent triggered by the input bot
        :param bot_id: Specific Bot to execute APIs against
        :param start_dt: Start of time filter
        :param end_dt: End of time filter
        :param utc_offset: Offset from GMT
        :param page: Number of page results to fetch
        :param per_page: Number of results per page
        :return:
        """
        url = "https://{0}/dashboard/bots_audience_lists/result_by_filters.json".format(self._endpoint)

        payload = {
            'per_page': per_page,
            'page': page,
            'bot_ids': [bot_id],
            'intent_types': [],
            'start_date': start_dt.strftime(API_DATE_FORMAT),
            'end_date': end_dt.strftime(API_DATE_FORMAT),
            'utc_offset': utc_offset
        }
        headers = {
            'Access-Token': self._access_token,
            'accept-encoding': "gzip, deflate, br",
            'content-type': "application/json;charset=UTF-8",
            'accept': "application/json"
        }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()

        return response.text

    def get_conversation(self, conversation_id, page=1, per_page=100):
        """
        :param conversation_id: Specific Bot to execute APIs against
        :param page: Number of page results to fetch
        :param per_page: Number of results per page
        :return:
        """
        url = "https://{0}/conversations/{1}/messages.json".format(self._endpoint, conversation_id)

        querystring = {
            "per_page": per_page,
            "page": page
        }

        headers = {
            'Access-Token': self._access_token,
            'accept-encoding': "gzip, deflate, br",
            'accept': "application/json",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()

        return response.text

