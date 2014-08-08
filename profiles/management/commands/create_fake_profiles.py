import logging
logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand

from shared.testing.factories.account import create_accounts
from profiles.tools.mentors import get_number_of_mentors

DESIRED_TOTAL_NUMBER_OF_MENTORS = 50


class Command(BaseCommand):

    def handle(self, *args, **options):
        current_number_of_mentors = get_number_of_mentors()
        number = DESIRED_TOTAL_NUMBER_OF_MENTORS - current_number_of_mentors

        if number < 1:
            logger.info('There are already %s mentors on the platform. Not generating any more' % DESIRED_TOTAL_NUMBER_OF_MENTORS)

        create_accounts(number)
