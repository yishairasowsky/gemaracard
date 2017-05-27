from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render

from django.utils import timezone

from .forms import FlashcardForm
from .models import Flashcard

@login_required
def delete(request, pk):
    Flashcard.objects.get(pk=pk).delete()
    return render(request, 'delete-alert.html')

@login_required
def flashcard_new(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            # commit=False b/c we want to add more data
            card = form.save(commit=False)
            # add in once we have authentication
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
    # return HttpResponse("Hello, world. You're at the flashcard index.")
    return render(request, 'index.html')
