from django.core.management.base import BaseCommand

# We work with JSON
import json


import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import job JSON result file (json_results)"

    def add_arguments(self, parser):
        parser.add_argument('json', nargs='+')

    def handle(self, *args, **options):
        for f in options["json"]:
            self.import_file(f)

    def import_file(self, filename):
        data = None
        try:
            with open(filename, "r") as f:
                data = json.loads(f.read())
        except IOError:
            logger.exception("Error reading json file '{0}'".format(filename))    

        if not data:
            logger.error("No data in file '{0}'".format(filename))
            return

        logger.info("Data {0}".format(data))
