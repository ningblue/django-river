import os
import sys

from django.test.utils import override_settings

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.core.management import call_command
from django.test import TestCase

_author_ = 'ahmetdal'


class TestMissingMigrations(TestCase):
    """
    This is the case to detect missing migration issues like https://github.com/javrasya/django-river/issues/30
    """

    migrations_before = []
    migrations_after = []

    def tearDown(self):
        """
            Remove migration file generated by test if there is any missing.
        """

        diff = list(set(self.migrations_after) - set(self.migrations_before))
        for d in diff:
            os.remove(os.path.join('river/migrations', d))

    @override_settings(MIGRATION_MODULES={})
    def test_missing_migrations(self):
        self.migrations_before = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/migrations/')))

        out = StringIO()
        sys.stout = out

        call_command('makemigrations', 'river', stdout=out)

        self.migrations_after = list(filter(lambda f: f.endswith('.py') and f != '__init__.py', os.listdir('river/migrations/')))

        self.assertEqual("No changes detected in app 'river'\n", out.getvalue())

        self.assertEqual(len(self.migrations_before), len(self.migrations_after))
