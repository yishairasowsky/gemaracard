from django.db import models
from django.contrib.auth.models import User


class Flashcard(models.Model):
    vocab_term = models.CharField(max_length=200, blank=False)
    HEBREW = 'HEB'
    ARAMAIC = 'ARAM'
    LOANWORD = 'LW'
    LANGUAGE_CHOICES = (
        (HEBREW, 'Hebrew'),
        (ARAMAIC, 'Aramaic'),
        (LOANWORD, 'Loanword')
    )
    language = models.CharField(
        max_length=4,
        choices=LANGUAGE_CHOICES,
        default=HEBREW,
    )
    loanword_language = models.TextField(blank=True)
    VERB = 'VERB'
    NOUN = 'NOUN'
    ADJECTIVE = 'ADJ'
    PREPOSITION = 'PREP'
    ADVERB = 'ADV'
    OTHER = 'OTHER'
    POS_CHOICES = (
        (VERB, 'Verb'),
        (NOUN, 'Noun'),
        (ADJECTIVE, 'Adjective'),
        (PREPOSITION, 'Preposition'),
        (ADVERB, 'Adverb'),
        (OTHER, 'Other'),
    )
    part_of_speech = models.CharField(
        max_length=5,
        choices=POS_CHOICES,
        default=NOUN,
    )
    root = models.CharField(max_length=4, blank=True)
    page_number = models.IntegerField(blank=True, default=0)
    translation = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.vocab_term

    def __unicode__(self):
        return self.vocab_term

class Text(models.Model):
    text = models.TextField(blank=False)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    flashcards = models.ManyToManyField(Flashcard)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
