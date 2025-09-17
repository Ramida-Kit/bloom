
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Joke, Topper

@login_required
def category_detail(request, category_id):
	category = get_object_or_404(Category, id=category_id, user=request.user)
	jokes = category.jokes.order_by('order')
	return render(request, 'jokes/category_detail.html', {
		'category': category,
		'jokes': jokes
	})
