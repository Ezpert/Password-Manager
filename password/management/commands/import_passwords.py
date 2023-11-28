from django.core.management.base import BaseCommand, CommandError
import csv
from password.models import Passwords


class Command(BaseCommand):
    help = 'Import passwords from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                password = Passwords.objects.create(
                    name=row[0],
                    url=row[1],
                    username=row[2],
                    password=row[3],
                )
