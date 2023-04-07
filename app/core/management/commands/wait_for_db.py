""""
Django commadn to wait for the database to be available
"""

import time

from psycopg2 import OperationalError as Psycopgs2pError

# error Django throws when db is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    # Unnamed values go in *args. Keyword arguments go in **options
    def handle(self, *args, **options):
        """Entrypoint for command"""

        # write that on the command line
        self.stdout.write('Waiting for database...')
        db_up = False

        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopgs2pError, OperationalError):
                self.stdout.write(
                    "Database unavailable, waiting for 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
