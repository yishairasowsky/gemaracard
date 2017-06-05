from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase, override_settings
from django.core.urlresolvers import resolve
# from django.test.client import RequestFactory
from django.test import RequestFactory
from django.core.urlresolvers import reverse

from .forms import FlashcardForm
from .models import Flashcard
from .views import flashcard_new, index

# to run: $ ./manage.py test
# Create your tests here.
# https://docs.djangoproject.com/en/1.11/intro/tutorial05/
# https://docs.djangoproject.com/en/1.9/topics/testing/advanced/#example
# http://toastdriven.com/blog/2011/apr/17/guide-to-testing-in-django-2/

# override less compression for tests
@override_settings(COMPRESS_PRECOMPILERS=())
class GemaraCardTest(TestCase):
    def setUp(self):
        # self.factory = RequestFactory()
        self.c = Client()
        pass

    def test_home(self):
        resp = self.c.get('/')
        content = resp.content
        self.assertIn(b'It\'s too hard to remember all these darn words. Make it simple!', content)
        self.assertEqual(resp.status_code, 200)

    def test_resolve_index(self):
        f = resolve('/')
        self.assertEqual(f.view_name, 'index')

    # def test_init_form(self):
    #     f = Flashcard.objects.all()[0]
    #     form = FlashcardForm(instance=f)
    #     self.assertTrue(isinstance(form.instance, Flashcard))
    #
    # def test_flashcard(self):
    #     flashcard = Flashcard.objects.all()[0]
    #     self.assertTrue(isinstance(flashcard, Flashcard))

@override_settings(COMPRESS_PRECOMPILERS=())
class LoggedInGemaraCardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='pass@123', email='test@test.com')
        # create request factory
        self.request_factory = RequestFactory()
        # create client with logged in user
        self.c = Client()
        self.c.force_login(self.user)
        # self.c.force_login(User.objects.get_or_create(username='test', password='pass@123', email='test@test.com')[0])
        self.test_flashcard = Flashcard.objects.create(vocab_term='חי', author_id=1)

    def test_flashcard_create_route(self):
        resp = self.c.get('/flashcard/new/')
        self.assertEqual(resp.status_code, 200)

    def test_create_flashcard_in_db(self):
        Flashcard.objects.create(vocab_term='מקור', author_id=1)
        flashcards = Flashcard.objects.all()
        self.assertEqual(len(flashcards), 2)
        found_card_arr = Flashcard.objects.filter(vocab_term='מקור')
        found_card = found_card_arr[0]
        self.assertEqual(found_card.vocab_term, 'מקור')

    def test_create_flashcard_through_post(self):
        # form = FlashcardForm({'vocab_term': 'אב',
        #                       'author_id': 1,
        #                       'translation': 'father',
        #                       'language': 'HEB',
        #                       'part_of_speech': 'NOUN'
        #                      })
        # self.assertTrue(form.is_valid())
        # https://stackoverflow.com/questions/9448038/accessing-the-request-user-object-when-testing-django
        # card = form.save()
        # self.assertEqual(card.vocab_term, 'אב')
        # resp = self.c.post('/flashcard/new/', {'vocab_term': 'אב', 'author_id': 1})
        # self.assertEqual(resp.status_code, 200)
        # found_card_arr = Flashcard.objects.filter(vocab_term='אב')
        # found_card = found_card_arr[0]
        # self.assertEqual(found_card.vocab_term, 'אב')
        request = self.request_factory.post('/flashcard/new/', {'vocab_term': 'אב',
                              'translation': 'father',
                              'language': 'HEB',
                              'part_of_speech': 'NOUN'
                             })
        request.user = self.user
        response = flashcard_new(request)
        self.assertEqual(response.status_code, 302)
        found_card_arr = Flashcard.objects.filter(vocab_term='אב')
        found_card = found_card_arr[0]
        self.assertEqual(found_card.vocab_term, 'אב')
