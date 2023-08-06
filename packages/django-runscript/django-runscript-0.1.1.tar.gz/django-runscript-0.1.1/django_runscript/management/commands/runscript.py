import logging
from argparse import ArgumentParser

from django.core.management import BaseCommand

from django_runscript.decorators import daemon, parallel
from django_runscript.utilities import import_script


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('script_path', nargs='?')
        parser.add_argument('-d', '--daemon', action='store_true')
        parser.add_argument('-i', '--interval', default=5, type=float)
        parser.add_argument('-c', '--concurrency', default=1, type=int)
        parser.add_argument('-l', '--logger', type=str)

    def handle(self, *args, script_path: str, **options):
        if script_path is None:
            raise ValueError('Script path required.')

        run_script = import_script(script_path)

        if options['logger'] is not None:
            options['logger'] = logging.getLogger(options['logger'])

        if options['daemon']:
            run_script = daemon(run_script, options['interval'], options['logger'])

        if options['concurrency'] > 1:
            run_script = parallel(run_script, options['concurrency'], options['logger'])

        run_script()
