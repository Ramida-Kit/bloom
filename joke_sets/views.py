
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JokeSet, JokeSetJoke

@login_required
def joke_set_detail(request, set_id):
	joke_set = get_object_or_404(JokeSet, id=set_id, user=request.user)
	joke_items = joke_set.joke_items.order_by('order')
	return render(request, 'joke_sets/joke_set_detail.html', {
		'joke_set': joke_set,
		'joke_items': joke_items
	})
