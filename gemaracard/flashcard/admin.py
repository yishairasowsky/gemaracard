from django.contrib import admin

from .models import Flashcard
from .forms import FlashcardForm

# admin.site.register(FlashcardForm)
admin.site.register(Flashcard)
