import json
import re

from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from thing.models import Tweet


handle_re = re.compile('^(@\w+ )*')

class Command(BaseCommand):
    help = 'Imports tweets'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        with open(options['file'], mode='r') as f:
            data = json.loads(f.read())

        for tweet in data:
            full_text = handle_re.sub('', tweet['full_text'])
            try:
                Tweet.objects.create(
                    slack_id=tweet['id'],
                    author_id=tweet['author_id'],
                    author_handle=tweet['author_handle'],
                    created_at=tweet['created_at'],
                    favorite_count=tweet['favorite_count'],
                    full_text=full_text
                )
                print(f'added: {full_text} ')
            except IntegrityError:
                pass  # print(f'Already exists: {full_text} ')
