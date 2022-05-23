from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from masters_app.models import Player

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class PlayerChoices(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_1", default=Player.objects.all().filter(id=1).values()[0]["player_name"]
    )
    player_2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_2", default=Player.objects.all().filter(id=2).values()[0]["player_name"]
    )
    player_3 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_3", default=Player.objects.all().filter(id=3).values()[0]["player_name"]
    )
    predicted_score = models.IntegerField(default=5)
    
    class Meta:
        app_label = 'masters_app'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        

class ESPN(models.Model):
    pos = models.TextField()
    player = models.OneToOneField(
        Player, on_delete=models.CASCADE, to_field="player_name", db_column="player", unique=True
    )
    country_flag_image = models.TextField()
    link = models.TextField()
    to_par = models.TextField()
    today = models.TextField()
    thru = models.TextField()
    r1 = models.TextField()
    r2 = models.TextField()
    r3 = models.TextField()
    r4 = models.TextField()
    tot = models.TextField()
    row_num = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'masters_espn'

class Scores(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    image = models.TextField()
    user_name = models.TextField()
    player_1 = models.TextField()
    player_2 = models.TextField()
    player_3 = models.TextField()
    score = models.IntegerField()
    predicted_score = models.IntegerField()

    class Meta:
        managed=False
        db_table = 'masters_app_scores'
