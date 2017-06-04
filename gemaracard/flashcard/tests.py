from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from .forms import FlashcardForm
from .models import Flashcard
from .views import index

# to run: $ ./manage.py test
# Create your tests here.
# https://docs.djangoproject.com/en/1.11/intro/tutorial05/
# https://docs.djangoproject.com/en/1.9/topics/testing/advanced/#example
class GemaraCardTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home(self):
        # c = Client()
        # resp = c.get('/')
        # https://docs.djangoproject.com/en/1.11/topics/testing/advanced/
        # request = self.factory.get('/')
        # resp = index(request)
        # resp = self.client.get('/')
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    def test_init_form(self):
        f = Flashcard.objects.all()[0]
        form = FlashcardForm(instance=f)
        self.assertTrue(isinstance(form.instance, Flashcard))

    def test_flashcard(self):
        flashcard = Flashcard.objects.all()[0]
        self.assertTrue(isinstance(flashcard, Flashcard))
