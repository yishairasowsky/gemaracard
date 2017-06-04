from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import UpdateView

from django.utils import timezone

from .forms import FlashcardForm, TextForm
from .models import Flashcard, User, Text

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
        card = Flashcard.objects.get(pk=pk, author=request.user)
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

@login_required
def text_new(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            text.user = request.user
            text.save()
            return redirect('text_detail', pk=text.pk)
    else:
        form = TextForm()
    return render(request, 'text-form.html', {'form': form})

@login_required
def text_list(request):
    texts = Text.objects.filter(user=request.user)
    sorted_texts = texts.order_by('name')
    context = {'texts': sorted_texts}
    return render(request, 'text-list.html', context)

@login_required
def text_detail(request, pk):
    try:
        text = Text.objects.get(pk=pk)
    except Text.DoesNotExist:
        raise Http404
    text_flashcards = text.flashcards.all()
    user_flashcards = Flashcard.objects.filter(author=request.user)
    context = {'text': text, 'text_flashcards': text_flashcards, 'user_flashcards': user_flashcards}
    return render(request, 'text.html', context)

@login_required
def link_flashcard_and_text(request, text_pk, card_pk):
    try:
        card = Flashcard.objects.get(pk=card_pk, author=request.user)
    except Flashcard.DoesNotExist:
        raise Http404
    try:
        text = Text.objects.get(pk=text_pk, user=request.user)
    except Text.DoesNotExist:
        raise Http404
    text.flashcards.add(card)
    # text_detail(request, text_pk)
    return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')
