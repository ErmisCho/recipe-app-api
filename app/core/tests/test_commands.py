"""
Test custom Django management commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error


from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# the check method is part of the BaseCommand Class
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    # patched_check: is coming from the @patch
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        # checks command is set up correctly and can be called
        call_command("wait_for_db")

        patched_check.assert_called_once_with(database=["default"])

    # with this the actual execution time is not going to be increased
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""

        # The first two times when the mocked method is called
        # expect 2 "Psycopg2Errors" and then 3 "OperationalErrors"
        # Psycopg2Error: application hasn't started yet, so it's not ready to accept connections
        # OperationalError: the testing database has not been set up yet
        # [True]: 6th time the mocked method is going to return "True"
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        # this method should be called 6 times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(database=["default"])
