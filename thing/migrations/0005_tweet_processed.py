# Generated by Django 3.1.6 on 2021-02-03 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thing', '0004_auto_20210202_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
