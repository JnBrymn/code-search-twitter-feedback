from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from thing.models import Topic, Tweet

#TODO! create summary page that lets you click into a list page

def classify(request, tweet_id=None):
    if tweet_id is None:
        return redirect(f'/classify/{Tweet.next_unprocessed().slack_id}')
    tweet = Tweet.objects.get(slack_id=tweet_id)
    if request.method == 'POST':
        topics = Topic.objects.filter(short_name__in=request.POST.keys())
        tweet.topics.clear()
        tweet.topics.add(*topics)
        tweet.processed = True
        tweet.save()
        return redirect(f'/classify/{Tweet.next_unprocessed().slack_id}')
    else:  # GET
        topics = Topic.objects.annotate(num=Count('tweets')).annotate(favs=Sum('tweets__favorite_count')).order_by('-num')
        checked = {t.short_name for t in tweet.topics.all()}
        context = {
            'unprocessed': Tweet.unprocessed_count(),
            'tweet': tweet,
            'topics': topics,
            'checked': checked,
        }
        template = loader.get_template('thing/classify.html')
        return HttpResponse(template.render(context, request))


def summary(request):
    topics = Topic.objects.annotate(num=Count('tweets')).annotate(favs=Sum('tweets__favorite_count')).order_by('-favs')
    context = {'topics': topics}
    template = loader.get_template('thing/summary.html')
    return HttpResponse(template.render(context, request))


def list(request):
    if request.method == 'POST':
        musts = get_must_must_not_topics(request.POST, 'must')
        must_nots = get_must_must_not_topics(request.POST, 'must_not')
        text = request.POST.get('text', '')
        return redirect(f'/list/?must={musts}&must_not={must_nots}&text={text}')
    else:  # GET
        musts = remove_empty_str(request.GET.get('must', '').split(','))
        must_nots = remove_empty_str(request.GET.get('must_not', '').split(','))
        text = request.GET.get('text','')

    tweets = Tweet.objects.all()

    for must in musts:
        tweets = tweets.filter(topics__short_name=must)
    if must_nots:
        tweets = tweets.exclude(topics__short_name__in=must_nots)
    if text:
        tweets = tweets.filter(full_text__contains=text)

    tweets = tweets.order_by('-favorite_count', 'created_at')
    topics = Topic.objects.all().annotate(favs=Sum('tweets__favorite_count')).order_by('-favs')
    context = {
        'musts': musts,
        'must_nots': must_nots,
        'text': text,
        'num': tweets.count(),
        'topics': topics,
        'tweets': tweets,
    }
    template = loader.get_template('thing/list.html')
    return HttpResponse(template.render(context, request))


def remove_empty_str(strings):
    return [s for s in strings if s != '']

def get_must_must_not_topics(post, must_or_must_not):
    assert must_or_must_not in ['must', 'must_not']
    topics = [t.split('.') for t in post]
    topics = [t[1] for t in topics if t[0] == must_or_must_not]
    topics = ','.join(topics)
    return topics
