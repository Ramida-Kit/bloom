
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from .models import JokeSet, JokeSetJoke
from jokes.models import Category, Joke, Topper

@login_required
def joke_set_detail(request, set_id):
	joke_set = get_object_or_404(JokeSet, id=set_id, user=request.user)
	categories = Category.objects.filter(user=request.user).prefetch_related('jokes__toppers')
	
	# Get current joke set items ordered by order field
	joke_set_items = joke_set.joke_items.select_related('joke__category').prefetch_related('toppers').order_by('order')
	
	if request.method == 'POST':
		action = request.POST.get('action')
		
		if action == 'add_joke':
			joke_id = request.POST.get('joke_id')
			if joke_id:
				joke = get_object_or_404(Joke, id=joke_id, category__user=request.user)
				# Get the highest order number and add 1
				max_order = joke_set.joke_items.aggregate(models.Max('order'))['order__max'] or 0
				joke_set_joke, created = JokeSetJoke.objects.get_or_create(
					joke_set=joke_set,
					joke=joke,
					defaults={'order': max_order + 1}
				)
		
		elif action == 'remove_joke':
			item_id = request.POST.get('item_id')
			if item_id:
				JokeSetJoke.objects.filter(id=item_id, joke_set=joke_set).delete()
		
		elif action == 'add_topper':
			item_id = request.POST.get('item_id')
			topper_id = request.POST.get('topper_id')
			if item_id and topper_id:
				item = get_object_or_404(JokeSetJoke, id=item_id, joke_set=joke_set)
				topper = get_object_or_404(Topper, id=topper_id)
				item.toppers.add(topper)
		
		elif action == 'remove_topper':
			topper_id = request.POST.get('topper_id')
			item_id = request.POST.get('item_id')
			if topper_id and item_id:
				item = get_object_or_404(JokeSetJoke, id=item_id, joke_set=joke_set)
				topper = get_object_or_404(Topper, id=topper_id)
				item.toppers.remove(topper)
		
		elif action == 'update_order':
			# Handle drag and drop reordering
			joke_orders = request.POST.get('joke_orders', '')
			if joke_orders:
				orders = joke_orders.split(',')
				for i, item_id in enumerate(orders):
					if item_id:
						JokeSetJoke.objects.filter(id=item_id, joke_set=joke_set).update(order=i)
		
		return redirect('joke_sets:joke_set_detail', set_id=joke_set.id)
	
	context = {
		'joke_set': joke_set,
		'joke_set_items': joke_set_items,
		'categories': categories,
	}
	return render(request, 'joke_sets/joke_set_detail.html', context)

@login_required
def add_joke_to_set(request, set_id):
	"""Add a joke to a joke set via AJAX"""
	if request.method == 'POST':
		joke_set = get_object_or_404(JokeSet, id=set_id, user=request.user)
		joke_id = request.POST.get('joke_id')
		
		if joke_id:
			joke = get_object_or_404(Joke, id=joke_id, category__user=request.user)
			# Get the highest order number and add 1
			max_order = joke_set.joke_items.aggregate(models.Max('order'))['order__max'] or 0
			joke_set_joke, created = JokeSetJoke.objects.get_or_create(
				joke_set=joke_set,
				joke=joke,
				defaults={'order': max_order + 1}
			)
			
			if created:
				return JsonResponse({'success': True, 'message': 'Joke added to set'})
			else:
				return JsonResponse({'success': False, 'message': 'Joke already in set'})
		
		return JsonResponse({'success': False, 'message': 'No joke selected'})
	
	return JsonResponse({'success': False, 'message': 'Invalid request method'})
