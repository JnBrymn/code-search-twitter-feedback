# Generated by Django 3.1.6 on 2021-02-02 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0002_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='tweets',
            field=models.ManyToManyField(related_name='topics', to='thing.Tweet'),
        ),
    ]
