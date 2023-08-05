import csv
import json
import logging
from urllib.parse import urlparse
from avaamo import CLI
from avaamo import BotController

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SendBotMessage(CLI):
    """
    This command line tool can be used to send a message to a bot and get the JSON output
    """

    def __init__(self):
        super(CLI, self).__init__()
        self._message = None

    def get_description(self):
        return "Sends a text message to a virtual assistant for testing"

    def add_arguments(self):
        self.parser.add_argument('-m', '--message', action='store', dest='message',
                                 metavar='text', required=True, help="Message to send to virtual assistant")

    def get_arguments(self):
        """
        Extract the command line arguments from the Namespace provide by argparse
        :return: None
        """
        logger.debug(self.args)
        self._message = self.args.message

    def send_message(self):
        controller = BotController()
        response = controller.send_message(self._message)
        return response

    def execute(self):
        self.initialize()
        print(json.dumps(self.send_message()))

    def run(self):
        self.execute()


def main():
    cli = SendBotMessage()
    cli.run()


if __name__ == '__main__':
    main()
