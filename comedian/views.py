from django.shortcuts import render
from jokes.models import Category
from joke_sets.models import JokeSet
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    categories = Category.objects.filter(user=request.user)
    joke_sets = JokeSet.objects.filter(user=request.user)
    return render(request, 'main.html', {
        'categories': categories,
        'joke_sets': joke_sets
    })
