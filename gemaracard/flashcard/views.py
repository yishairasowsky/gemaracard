from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import UpdateView

from django.utils import timezone

from .forms import FlashcardForm
from .models import Flashcard, User

@login_required
def delete(request, pk):
    Flashcard.objects.get(pk=pk).delete()
    return render(request, 'delete-alert.html')

# class FlashcardUpdate(UpdateView):
#     model = Flashcard
#     template = 'edit-flashcard.html'
#
#     def get_success_url(self):
#         return reverse('flashcard_list')

@login_required
def edit(request, pk):
    instance = Flashcard.objects.get(pk=pk)
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=instance)
        if form.is_valid():
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
