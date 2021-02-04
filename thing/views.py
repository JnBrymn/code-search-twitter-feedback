from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from thing.models import Topic, Tweet

def classify(request, tweet_id=None):
    #TODO! order topic by popularity and add number to list items
    #TODO! next tweet link is based on random sample of unfinished (so that you can hit back in browser)
    if tweet_id is None:
        return redirect(f'/{Tweet.next_unprocessed().slack_id}')
    tweet = Tweet.objects.get(slack_id=tweet_id)
    if request.method == 'POST':
        topics = Topic.objects.filter(short_name__in=request.POST.keys())
        tweet.topics.clear()
        tweet.topics.add(*topics)
        tweet.processed = True
        tweet.save()
        return redirect(f'/{Tweet.next_unprocessed().slack_id}')
    else: # GET
        topics = Topic.objects.annotate(num=Count('tweets')).annotate(favs=Sum('tweets__favorite_count')).order_by('-favs')
        checked = {t.short_name for t in tweet.topics.all()}
        context = {
            'unprocessed': Tweet.unprocessed_count(),
            'tweet': tweet,
            'topics': topics,
            'checked': checked,
        }
        template = loader.get_template('thing/classify.html')
        return HttpResponse(template.render(context, request))


def list(request):
    #TODO string search
    #TODO list sorted by favorite then date
    #TODO link out to their classify page
    topics = Topic.objects.annotate(num=Count('tweets')).order_by('-num')

    must = remove_empty_str(request.GET.get('must', '').split(','))
    must_not = remove_empty_str(request.GET.get('must_not', '').split(','))

    tweets = Tweet.objects.all()

    # for m in must:
    #     tweets.filter(topics__short_name)
    context = {
        'topics': topics
    }
    template = loader.get_template('thing/list.html')
    return HttpResponse(template.render(context, request))

def remove_empty_str(strings):
    return [s for s in strings if s != '']