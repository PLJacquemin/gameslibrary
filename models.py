import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
# appid;name;playtime_forever;img_icon_url;completed;played;date

class Video_game(models.Model):
    name = models.CharField('Name',max_length=100,)
    playtime_forever = models.IntegerField('Playtime',default=0)
    img_icon_url = models.CharField('Icon URL',max_length=250,default='')
    completed = models.BooleanField('Finished',default=False)
    played = models.BooleanField('Launched',default=False)
    date = models.DateField('Finish date', default="2020-01-01")
    genre = models.CharField('Genre',max_length=40,default='')
    platform = models.CharField('Platform',max_length=40,default='')
    appid = models.CharField('Appid',max_length=40,default=0)
    last_played = models.DateField('Last played', default="2020-01-01")
    img_url = models.CharField('Image URL',max_length=250,default='')
    def __str__(self):
        return self.name
