from django.conf.urls import url

from flashcard.views import flashcard_new, index

urlpatterns = [
  url(r'^$', index, name='index'),
  url(r'^flashcard/new/$', flashcard_new, name='flashcard_new')
]
