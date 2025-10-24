from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='categories')
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Joke(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jokes')
	name = models.CharField(max_length=100)
	setup = models.TextField()
	punchline = models.TextField()
	runtime = models.PositiveIntegerField(help_text='Runtime in seconds')
	order = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Topper(models.Model):
	joke = models.ForeignKey(Joke, on_delete=models.CASCADE, related_name='toppers')
	text = models.TextField()
	order = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"Topper for {self.joke.name}: {self.text[:30]}"

class JokeSet(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class JokeSetItem(models.Model):
    joke_set = models.ForeignKey(JokeSet, on_delete=models.CASCADE, related_name='items')
    joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ['joke_set', 'joke']

class JokeSetTopper(models.Model):
    joke_set_item = models.ForeignKey(JokeSetItem, on_delete=models.CASCADE, related_name='selected_toppers')
    topper = models.ForeignKey(Topper, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        unique_together = ['joke_set_item', 'topper']
