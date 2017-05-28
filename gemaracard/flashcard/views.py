from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import UpdateView

from django.utils import timezone

from .forms import FlashcardForm
from .models import Flashcard, User

def set_optional_fields(card):
    if card.language != 'LW':
        card.loanword_language = ''
    return card

@login_required
def delete(request, pk):
    Flashcard.objects.get(pk=pk).delete()
    return render(request, 'delete-alert.html')

@login_required
def edit(request, pk):
    instance = Flashcard.objects.get(pk=pk)
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # go back and correct the optional fields
            form = set_optional_fields(instance)
            form.save()
            return redirect('flashcard_detail', pk=pk)
    else:
        form = FlashcardForm(request.POST or None, instance=instance)
        return render(request, 'flashcard-form.html', {'form': form})

@login_required
def flashcard_new(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            # commit=False b/c we want to add more data
            card = form.save(commit=False)
            # validate extra optional fields
            card = set_optional_fields(card)
            card.author = request.user
            card.published_date = timezone.now()
            card.save()
            return redirect('flashcard_detail', pk=card.pk)
    else:
        form = FlashcardForm()
    return render(request, 'flashcard-form.html', {'form': form})

@login_required
def flashcard_detail(request, pk):
    try:
        card = Flashcard.objects.get(pk=pk)
    except Flashcard.DoesNotExist:
        raise Http404
    context = {'card': card}
    return render(request, 'flashcard.html', context)

@login_required
def flashcard_list(request):
    flashcards = Flashcard.objects.filter(author=request.user)
    sorted_flashcards = flashcards.order_by('vocab_term')
    context = {'cards': sorted_flashcards}
    return render(request, 'flashcard-list.html', context)

def index(request):
    return render(request, 'index.html')
