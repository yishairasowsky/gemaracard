from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .forms import FlashcardForm

def flashcard_new(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            # commit=False b/c we want to add more data
            post = form.save(commit=False)
            # add in once we have authentication
            # card.author = request.user
            post.published_date = timezone.now()
            post.save()
    else:
        form = FlashcardForm()
    return render(request, 'flashcard-form.html', {'form': form})

def index(request):
    # return HttpResponse("Hello, world. You're at the flashcard index.")
    return render(request, 'index.html')


def get_name(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = FlashcardForm()

    return render(request, 'flashcard-form.html', {'form': form})
