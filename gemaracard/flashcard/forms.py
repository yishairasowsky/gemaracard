from django import forms
from .models import Flashcard

class FlashcardForm(forms.ModelForm):
    LANGUAGE_CHOICES = (
        ('HEB', 'Hebrew',),
        ('ARAM', 'Aramaic',),
        ('LW', 'Loanword',)
    )
    language = forms.ChoiceField(widget=forms.Select, choices=LANGUAGE_CHOICES)
    class Meta:
        model = Flashcard
        fields = ('vocab_term','language', 'part_of_speech', 'root',
                  'page_number', 'translation', 'notes',)
    # http://stackoverflow.com/questions/24783275/django-form-with-choices-but-also-with-freetext-option
    # BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
    # birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # dictionary = forms.MultipleChoiceField(widget=forms.CheckboxInput)
    # your_name = forms.CharField(label='your name', max_length=100)
