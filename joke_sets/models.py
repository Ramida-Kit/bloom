
from django.db import models
from django.contrib.auth import get_user_model
from jokes.models import Joke, Topper

class JokeSet(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='joke_sets')
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class JokeSetJoke(models.Model):
	joke_set = models.ForeignKey(JokeSet, on_delete=models.CASCADE, related_name='joke_items')
	joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
	order = models.PositiveIntegerField(default=0)
	toppers = models.ManyToManyField(Topper, blank=True)

	def __str__(self):
		return f"{self.joke_set.name} - {self.joke.name}"
