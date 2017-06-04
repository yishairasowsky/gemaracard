from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase, override_settings
from django.core.urlresolvers import resolve
# from django.test.client import RequestFactory
from django.test import RequestFactory
from django.core.urlresolvers import reverse

from .forms import FlashcardForm
from .models import Flashcard
from .views import index

# to run: $ ./manage.py test
# Create your tests here.
# https://docs.djangoproject.com/en/1.11/intro/tutorial05/
# https://docs.djangoproject.com/en/1.9/topics/testing/advanced/#example

# override less compression for tests
@override_settings(COMPRESS_PRECOMPILERS=())
class GemaraCardTest(TestCase):
    def setUp(self):
        # self.factory = RequestFactory()
        self.c = Client()
        pass

    def test_home(self):
        resp = self.c.get('/')
        # https://docs.djangoproject.com/en/1.11/topics/testing/advanced/
        # request = self.factory.get('/')
        # resp = index(request)
        # resp = self.client.get('/')
        # resp = self.client.get('/')
        content = resp.content
        self.assertIn(b'darn', content)
        self.assertEqual(resp.status_code, 200)

    def test_resolve(self):
        f = resolve('/')
        self.assertEqual(f.view_name, 'index')

    # verify that problem is in get
    def test_math(self):
        x = 25 * 4
        self.assertEqual(x, 100)

    # def test_init_form(self):
    #     f = Flashcard.objects.all()[0]
    #     form = FlashcardForm(instance=f)
    #     self.assertTrue(isinstance(form.instance, Flashcard))
    #
    # def test_flashcard(self):
    #     flashcard = Flashcard.objects.all()[0]
    #     self.assertTrue(isinstance(flashcard, Flashcard))
