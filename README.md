# get started

```sh
# rm db.sqlite3  # WARNING
unset DJANGO_SETTINGS_MODULE
./manage.py makemigrations
./manage.py migrate
./manage.py import_tweets response_data.json
./manage.py add_default_topics
```

```sh
./manage.py runserver
```


# todo 
* after fave count, sort by date desc
*Add URL parameter to filter down to specific topic (and see already processed ones) 
*^ including overlaps