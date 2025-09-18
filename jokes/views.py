
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
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


@login_required
def add_category(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		if name:
			Category.objects.create(user=request.user, name=name)
	return redirect('main')

@login_required
def add_joke(request, category_id):
	category = get_object_or_404(Category, id=category_id, user=request.user)
	if request.method == 'POST':
		name = request.POST.get('name')
		setup = request.POST.get('setup')
		punchline = request.POST.get('punchline')
		runtime = request.POST.get('runtime')
		toppers_text = request.POST.get('toppers', '')
		if name and setup and punchline and runtime:
			joke = Joke.objects.create(
				category=category,
				name=name,
				setup=setup,
				punchline=punchline,
				runtime=runtime
			)
			toppers = [t.strip() for t in toppers_text.splitlines() if t.strip()]
			for idx, topper_text in enumerate(toppers):
				Topper.objects.create(joke=joke, text=topper_text, order=idx)
	return redirect('category_detail', category_id=category.id)
@login_required
def edit_joke(request, joke_id):
	joke = get_object_or_404(Joke, id=joke_id)
	category = joke.category
	if request.method == 'POST':
		joke.name = request.POST.get('name')
		joke.setup = request.POST.get('setup')
		joke.punchline = request.POST.get('punchline')
		joke.runtime = request.POST.get('runtime')
		joke.save()
		toppers_text = request.POST.get('toppers', '')
		toppers = [t.strip() for t in toppers_text.splitlines() if t.strip()]
		# Remove old toppers and add new ones in order
		joke.toppers.all().delete()
		for idx, topper_text in enumerate(toppers):
			Topper.objects.create(joke=joke, text=topper_text, order=idx)
		return redirect('category_detail', category_id=category.id)
	return redirect('category_detail', category_id=category.id)
@login_required
def add_topper(request, joke_id):
	joke = get_object_or_404(Joke, id=joke_id)
	category = joke.category
	if request.method == 'POST':
		text = request.POST.get('text')
		if text:
			# Find the next order value
			max_order = joke.toppers.aggregate(max_order=models.Max('order'))['max_order'] or 0
			Topper.objects.create(joke=joke, text=text, order=max_order + 1)
	return redirect('category_detail', category_id=category.id)
