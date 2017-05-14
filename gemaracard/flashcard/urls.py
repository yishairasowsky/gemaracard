from django.conf.urls import url

from flashcard.views import flashcard_detail, flashcard_list, flashcard_new, index

urlpatterns = [
  url(r'^$', index, name='index'),
  url(r'^flashcard/new/$', flashcard_new, name='flashcard_new'),
  url(r'^flashcard/(?P<pk>\d+)/$', flashcard_detail, name='flashcard_detail'),
  url(r'^flashcard-list/$', flashcard_list, name='flashcard_list')
]
