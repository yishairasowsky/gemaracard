from django.conf.urls import url

from flashcard.views import delete, edit, flashcard_detail, flashcard_list, flashcard_modal, flashcard_new, index,link_flashcard_list, link_flashcard_and_text, text_detail, text_list, text_new

urlpatterns = [
  url(r'^$', index, name='index'),
  url(r'^flashcard/new/$', flashcard_new, name='flashcard_new'),
  url(r'^flashcard/(?P<pk>\d+)/$', flashcard_detail, name='flashcard_detail'),
  url(r'^flashcard/modal/(?P<pk>\d+)/$', flashcard_modal, name='flashcard_modal'),
  url(r'^flashcard-list/$', flashcard_list, name='flashcard_list'),
  url(r'^link-flashcard-list/(?P<text_pk>\d+)/$', link_flashcard_list, name='link_flashcard_list'),
  url(r'^delete/(?P<pk>\d+)/$', delete, name='delete'),
  url(r'^edit/(?P<pk>\d+)/$', edit, name='edit',),
  url(r'^text/new/$', text_new, name='text_new'),
  url(r'^text-list/$', text_list, name='text_list'),
  url(r'^text/(?P<pk>\d+)/$', text_detail, name='text_detail'),
  # need to remove $ ?
  url(r'^link/(?P<text_pk>\d+)/(?P<card_pk>\d+)/$', link_flashcard_and_text, name='link_flashcard_and_text'),
]
