from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db import models
from django.contrib.auth.decorators import login_required
from .models import Category, Joke, Topper, JokeSet, JokeSetItem, JokeSetTopper


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

def joke_sets(request):
    joke_sets = JokeSet.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            joke_set = JokeSet.objects.create(name=name)
            return redirect('joke_set_detail', joke_set_id=joke_set.id)
    
    return render(request, 'jokes/joke_sets.html', {'joke_sets': joke_sets})

def joke_set_detail(request, joke_set_id):
    joke_set = get_object_or_404(JokeSet, id=joke_set_id)
    categories = Category.objects.all()
    all_jokes = Joke.objects.all().select_related('category').prefetch_related('toppers')
    
    # Get current joke set items with their selected toppers
    joke_set_items = JokeSetItem.objects.filter(joke_set=joke_set).select_related('joke').prefetch_related('selected_toppers__topper')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_joke':
            joke_id = request.POST.get('joke_id')
            if joke_id:
                joke = get_object_or_404(Joke, id=joke_id)
                # Get the highest order number and add 1
                max_order = JokeSetItem.objects.filter(joke_set=joke_set).aggregate(models.Max('order'))['order__max'] or 0
                JokeSetItem.objects.get_or_create(
                    joke_set=joke_set,
                    joke=joke,
                    defaults={'order': max_order + 1}
                )
        
        elif action == 'remove_joke':
            item_id = request.POST.get('item_id')
            if item_id:
                JokeSetItem.objects.filter(id=item_id, joke_set=joke_set).delete()
        
        elif action == 'add_topper':
            item_id = request.POST.get('item_id')
            topper_id = request.POST.get('topper_id')
            if item_id and topper_id:
                item = get_object_or_404(JokeSetItem, id=item_id, joke_set=joke_set)
                topper = get_object_or_404(Topper, id=topper_id)
                # Get the highest order number for this item's toppers and add 1
                max_order = JokeSetTopper.objects.filter(joke_set_item=item).aggregate(models.Max('order'))['order__max'] or 0
                JokeSetTopper.objects.get_or_create(
                    joke_set_item=item,
                    topper=topper,
                    defaults={'order': max_order + 1}
                )
        
        elif action == 'remove_topper':
            topper_id = request.POST.get('topper_id')
            item_id = request.POST.get('item_id')
            if topper_id and item_id:
                JokeSetTopper.objects.filter(
                    id=topper_id,
                    joke_set_item__joke_set=joke_set
                ).delete()
        
        elif action == 'update_order':
            # Handle drag and drop reordering
            joke_orders = request.POST.get('joke_orders', '')
            if joke_orders:
                orders = joke_orders.split(',')
                for i, item_id in enumerate(orders):
                    if item_id:
                        JokeSetItem.objects.filter(id=item_id, joke_set=joke_set).update(order=i)
            
            topper_orders = request.POST.get('topper_orders', '')
            item_id = request.POST.get('item_id_for_toppers')
            if topper_orders and item_id:
                orders = topper_orders.split(',')
                for i, topper_set_id in enumerate(orders):
                    if topper_set_id:
                        JokeSetTopper.objects.filter(
                            id=topper_set_id,
                            joke_set_item_id=item_id
                        ).update(order=i)
        
        return redirect('joke_set_detail', joke_set_id=joke_set.id)
    
    context = {
        'joke_set': joke_set,
        'joke_set_items': joke_set_items,
        'categories': categories,
        'all_jokes': all_jokes,
    }
    return render(request, 'jokes/joke_set_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'jokes/category_list.html', {'categories': categories})
