from django.urls import path

from . import views

urlpatterns = [
    path('', views.summary, name='summary'),
    path('classify/', views.classify, name='classify'),
    path('classify/<int:tweet_id>', views.classify, name='classify'),
    path('list/', views.list, name='list'),
]
