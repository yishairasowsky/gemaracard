from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.core.urlresolvers import resolve
# from django.test.client import RequestFactory
from django.test import RequestFactory
from django.core.urlresolvers import reverse

from .forms import FlashcardForm
from .models import Flashcard, Text
from .views import flashcard_new, index, link_flashcard_and_text, text_new

# to run: $ ./manage.py test

# override less compression for tests
@override_settings(COMPRESS_PRECOMPILERS=())
class GemaraCardTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create(username='test', password='pass@123', email='test@test.com')

    def test_home(self):
        resp = self.c.get('/')
        content = resp.content
        self.assertIn(b'It\'s too hard to remember all these darn words. Make it simple!', content)
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.c.post('/login/', {'username': 'test', 'password': 'pass@123'})
        self.assertEqual(resp.status_code, 200)

    def test_resolve_index(self):
        f = resolve('/')
        self.assertEqual(f.view_name, 'index')

    def test_resolve_login(self):
        f = resolve('/login/')
        self.assertEqual(f.view_name, 'login')

    def test_resolve_register(self):
        f = resolve('/accounts/register/')
        self.assertEqual(f.view_name, 'accounts:registration_register')

@override_settings(COMPRESS_PRECOMPILERS=())
class LoggedInGemaraCardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='pass@123', email='test@test.com')
        # create request factory
        self.request_factory = RequestFactory()
        # create client with logged in user
        self.c = Client()
        self.c.force_login(self.user)
        self.test_flashcard = Flashcard.objects.create(vocab_term='חי', author_id=1)
        self.test_text = Text.objects.create(name='m. Berachot 1.2', user=self.user, text='מעשה שבאו בניו מבית המשתה, ואמרו לו, לא קרינו את שמע.  אמר להם, אם לא עלה עמוד השחר, מותרין אתם לקרות.')

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

    def test_logout(self):
        f = resolve('/logout/')
        self.assertEqual(f.view_name, 'logout')

    def test_create_text(self):
        request = self.request_factory.post('/text/new/', {
            'name': 'm. Berachot 1.1',
            'text': 'מאימתיי קורין את שמע בערבין:  משעה שהכוהנים נכנסין לאכול בתרומתן, עד סוף האשמורת הראשונה, דברי רבי אליעזר.  וחכמים אומרין, עד חצות.  רבן גמליאל אומר, עד שיעלה עמוד השחר.'
        })
        request.user = self.user
        response = text_new(request)
        self.assertEqual(response.status_code, 302)
        found_text_arr = Text.objects.all()
        found_text = found_text_arr[1]
        self.assertEqual(found_text.name, 'm. Berachot 1.1')

    def test_link_test(self):
        request = self.request_factory.get('/link/1/1/') # link text 1 and card 1
        request.user = self.user
        response = link_flashcard_and_text(request, 1, 1)
        self.assertEqual(response.status_code, 200)
        resp = self.c.get('/text/1/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        # assert that the text appears
        self.assertIn('מעשה שבאו', content)
        # assert that the flash card shows up
        self.assertIn('חי', content)
