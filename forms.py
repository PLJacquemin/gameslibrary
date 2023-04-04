from django import forms
from django.forms import ModelForm
from .models import Video_game

class GameForm(ModelForm):
    class Meta:
        model = Video_game
        fields = "__all__"
        #labels = {
        #    'name': '',
        #    'playtime_forever': '',
        #    "img_icon_url": '',
        #    "completed": '',
        #    "played": '',
        #    "date": '',
        #}
        widgets = {
            'appid': forms.TextInput(attrs={'class': "form-control"}),
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'playtime_forever': forms.TextInput(attrs={'class': "form-control"}),
            "img_icon_url": forms.TextInput(attrs={'class': "form-control"}),
            "completed": forms.CheckboxInput(attrs={'class':'form-check-input'}),
            "played": forms.CheckboxInput(attrs={'class':'form-check-input'}),
            "date": forms.DateInput({'class':'form-control','type':'date'}),
            "genre": forms.TextInput(attrs={'class': "form-control"}),
            "platform": forms.TextInput(attrs={'class': "form-control"}),
            "last_played": forms.DateInput({'class':'form-control','type':'date'}),
        }