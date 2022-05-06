from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    player_name = models.TextField(unique=True)
    odds_points = models.IntegerField()

    def __str__(self):
        return self.player_name
    
    class Meta:
        db_table = 'masters_app_player'
        constraints = [
            models.UniqueConstraint(fields=['player_name'], name='unique player')
        ]
