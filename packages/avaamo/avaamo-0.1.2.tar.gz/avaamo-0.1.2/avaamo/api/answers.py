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
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Answers(object):
    def __init__(self):
        try:
            self._access_token = os.environ['AVAAMO_ACCESS_TOKEN']
            self._end_point = os.environ['AVAAMO_END_POINT']
        except KeyError as e:
            logger.error(e)

    def default_headers(self, access_token):
        headers = {
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,ru;q=0.8",
            'accept': "application/json, text/plain, */*",
            'access-token': access_token
        }

    def add_document(self, kp_id, url, name):
        template_path = "https://{0}/dashboard/bot_knowledge_packs/{1}/knowledge_documents.json"
        end_point_url = template_path.format(self._end_point, kp_id)
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

    def list_document(self, kp_id):
        """
        TODO: Handle multiple pages
        :kp_id: Avaamo Answers knowledge pack id

        """
        template_path = "https://{0}/dashboard/bot_knowledge_packs/{1}/knowledge_documents.json"
        end_point_url = template_path.format(self._end_point, kp_id)
        headers = {
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,ru;q=0.8",
            'content-type': "application/json;charset=UTF-8",
            'accept': "application/json",
            'Access-Token': self._access_token
        }
        querystring = {
            "page": 1,
            "per_page": "1024"
        }

        logger.debug(headers)
        response = None
        try:
            response = requests.request("GET", end_point_url, headers=headers, params=querystring)
        except Exception as e:
            logger.exception(e)

        return response

    def test_document(self, kp_id, text, nlu=True, language='en-US'):
        """

        """
        template_path = "https://{0}/dashboard/bot_knowledge_packs/{1}/test_document.json"
        end_point_url = template_path.format(self._end_point, kp_id)
        document = {
            "text": "How do I start?",
            "language": language,
            "nlu": nlu
        }
        payload = json.dumps(document)
        logger.debug(payload)
        headers = {
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,ru;q=0.8",
            'accept': "application/json, text/plain, */*",
            'access-token': self._access_token
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
