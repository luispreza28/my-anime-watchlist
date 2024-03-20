from django.contrib.auth.models import AbstractUser
from django.db import models
from sklearn.feature_extraction.text import TfidfVectorizer

# Create your models here.
class User(AbstractUser):
  pass

class Genre(models.Model):
   name = models.CharField(max_length=50, unique=True)

   def __str__(self):
      return self.name

class Anime(models.Model):
  myanimelist_id = models.IntegerField(blank=True, null=True)
  description = models.TextField(blank=True, null=True, max_length=600)
  myanimelist_url = models.URLField(blank=True, null=True)
  title = models.CharField(max_length=255)
  rank = models.IntegerField(blank=True, null=True)
  picture_url = models.URLField(blank=True, null=True)
  score = models.IntegerField(blank=True, null=True)
  genre = models.ManyToManyField(Genre, blank=True)

  def __str__(self):
      return self.title

class UserAnimeList(models.Model):

  # choices for status field
  STATUS_CHOICES = [
     ('currently_watching', 'Currently Watching'),
     ('completed', 'Completed'),
     ('on_hold', 'On Hold'),
     ('dropped', 'Dropped'),
     ('plan_to_watch', 'Plan to Watch'),
  ]

  user = models.ForeignKey(User, related_name="user",on_delete=models.CASCADE)
  anime = models.ForeignKey(Anime, related_name="anime", on_delete=models.CASCADE)
  rating = models.IntegerField(blank=True, null=True)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="plan_to_watch")
  progress = models.IntegerField(blank=True,null=True)
  review = models.TextField(blank=True,null=True)
  myanimelist_id = models.IntegerField(blank=True,null=True)