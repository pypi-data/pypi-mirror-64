import requests
import json
import argparse
import os
import time
import csv
import logging
from urllib.parse import urlparse
from urllib.parse import quote
from avaamo import CLI
from avaamo import Answers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AddDocument(CLI):
    """
    This command line tool can be used to load a single document or URL into an existing
    Avaamo Answers knowledge pack. A batch of
    """

    def __init__(self):
        super(CLI, self).__init__()
        self._answers = Answers()
        self._batch_load = None
        self._kp_id = None
        self._document_type = None
        self._file_type = None
        self._name = None
        self._url = None
        self._sleep = None

    def get_description(self):
        return "Adds a URL or PDF document to a knowledge pack"

    def add_arguments(self):
        self.parser.add_argument('-k', '--knowledge-pack-id', action='store', dest='kp_id',
                                 metavar='id', required=True, help="Id of the knowledge pack to add the document")
        self.parser.add_argument('-b', '--batch-load', action='store_true', dest='batch_load', required=False,
                                 help="Indicates if the URL is a single URL or file to a bunch of URLs")
        self.parser.add_argument('-d', '--debug', action='store_true', dest='debug', required=False,
                                 help="URL or file to a bunch of URLs")
        self.parser.add_argument('-f', '--file-type', action='store', dest='file_type',
                                 type=str, choices=['plain', 'csv', 'json', 'xml'], required=False,
                                 help="Type of the file")
        self.parser.add_argument('-t', '--document-type', action='store', dest='document_type',
                                 metavar='type', type=str, choices=['url', 'pdf'], required=False,
                                 help="Either url or pdf")
        self.parser.add_argument('-u', '--url', action='store', dest='url', metavar='url', required=False,
                                 help="URL to web page or path to a file to load into knowledge pack")
        self.parser.add_argument('-n', '--name', action='store', dest='name', metavar='name', required=False,
                                 help="Name to use for the uploaded document")
        self.parser.add_argument('-s', '--sleep', action='store', dest='sleep', metavar='secs',
                                 default=0, type=int, required=False,
                                 help="How much time to pause between API calls in batch mode")

    def get_arguments(self):
        """
        Extract the command line arguments from the Namespace provide by argparse

        :return: None
        """
        logger.debug(self.args)
        self._batch_load = self.args.batch_load
        self._document_type = self.args.document_type
        self._file_type = self.args.file_type
        self._kp_id = self.args.kp_id
        self._name = self.args.name
        self._url = self.args.url
        self._sleep = self.args.sleep

    def pdf_upload(self, kp_id, file_path, name):
        """

        :param kp_id:
        :param file_path: Path to document
        :param name:
        :return:
        """
        pass

    def url_upload(self, kp_id, url, name):
        """
        TODO: Multi-language support

        :param kp_id: Knowledge Pack Identifier
        :param url: URL to add to the knowledge pack
        :param name: Name of the document displayed in the web interface
        :return:
        """
        self._answers.add_document(kp_id=kp_id, url=url, name=name)

    def process_documents(self):
        if self._batch_load:
            if self._file_type == 'plain':
                self.read_urls_from_file()
            elif self._file_type == 'csv':
                self.read_urls_from_csv_file()
            else:
                logger.error("Unsupported file type")
        else:
            self.url_upload(self._kp_id, self._url, self._name)

    def read_urls_from_file(self):
        """
        Read file of URLS and use the URL as the name.

        :return: None
        """
        url = urlparse(self._url)
        logger.debug("path: {0}".format(url.path))
        with open(url.path) as fp:
            lines = fp.readlines()
            for url in lines:
                url = url.strip()
                logger.debug("url: '{0}'".format(url))
                self.url_upload(kp_id=self._kp_id, url=url, name=url)
                time.sleep(self._sleep)

    def read_urls_from_csv_file(self):
        """
        :return: None
        """
        url = urlparse(self._url)
        logger.debug("path: {0}".format(url.path))
        with open(url.path) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                url = row['url']
                name = row['name']
                self.url_upload(kp_id=self._kp_id, url=url, name=name)

    def execute(self):
        self.initialize()
        self.process_documents()

    def run(self):
        self.execute()


def main():
    cli = AddDocument()
    cli.run()


if __name__ == '__main__':
    main()
