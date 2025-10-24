from django.shortcuts import render, redirect
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

@login_required
def add_joke_set(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            joke_set = JokeSet.objects.create(user=request.user, name=name)
            return redirect('joke_set_detail', set_id=joke_set.id)
    return redirect('main')
