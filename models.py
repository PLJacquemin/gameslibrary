import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Video_game(models.Model):
    name = models.CharField('Name',max_length=100,)
    playtime_forever = models.IntegerField('Playtime',default=0)
    img_icon_url = models.CharField('Icon URL',max_length=250,default='')
    completed = models.BooleanField('Finished',default=False)
    played = models.BooleanField('Launched',default=False)
    gaas = models.BooleanField('GAAS/MMO/Multi',default=False)
    unfinishable = models.BooleanField('Unfinishable (Sandbox, scoring...)',default=False)
    date = models.DateField('Finish date', default="2020-01-01")
    genre = models.CharField('Genre',max_length=40,default='')
    platform = models.CharField('Platform',max_length=40,default='')
    appid = models.CharField('Appid',max_length=40,default=0)
    last_played = models.DateField('Last played', default="2020-01-01")
    img_url = models.CharField('Image URL',max_length=250,default='')
    critic = models.CharField('Critic',max_length=500,default='',blank = True)
    num_stars = models.IntegerField('Stars',default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    publisher = models.CharField('Publisher',max_length=100,default='',blank = True)
    release_year = models.IntegerField('Release year',default=1900)
    update_date = models.DateField('Last updated', default="2020-01-01")
    
    def __str__(self):
        return self.name