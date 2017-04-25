from django.db import models

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
    # how do i change this so that loanword can display field?
    language = models.CharField(
        max_length=4,
        choices=LANGUAGE_CHOICES,
        default=HEBREW,
    )
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

    def __str__(self):
        return self.vocab_term
