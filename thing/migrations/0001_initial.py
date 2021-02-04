# Generated by Django 3.1.6 on 2021-02-02 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_id', models.CharField(max_length=50)),
                ('author_id', models.CharField(max_length=50)),
                ('author_handle', models.CharField(max_length=50)),
                ('created_at', models.IntegerField()),
                ('favorite_count', models.IntegerField()),
                ('full_text', models.CharField(max_length=300)),
            ],
        ),
    ]
