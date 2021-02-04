import json
from django.db import models


class Tweet(models.Model):
    slack_id = models.CharField(max_length=50, unique=True)
    author_id = models.CharField(max_length=50)
    author_handle = models.CharField(max_length=50)
    created_at = models.IntegerField()
    favorite_count = models.IntegerField()
    full_text = models.CharField(max_length=300)
    processed = models.BooleanField(default=False)

    def __repr__(self):
        return pprint_obj(self)

    @classmethod
    def next_unprocessed(cls):
        return cls.objects.filter(processed=False).order_by('-favorite_count', 'created_at').first()

    @classmethod
    def unprocessed_count(cls):
        return cls.objects.filter(processed=False).count()


class Topic(models.Model):
    description = models.CharField(max_length=200)
    short_name = models.CharField(max_length=40, unique=True)
    tweets = models.ManyToManyField(Tweet, related_name='topics')

    def __repr__(self):
        return pprint_obj(self)


def pprint_obj(obj):
    return json.dumps(
        {k: str(v) for k, v in obj.__dict__.items() if k[0] != '_'},
        indent=2,
    )