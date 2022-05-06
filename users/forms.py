from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from masters_app.models import Player
from .models import PlayerChoices, Profile
from django.forms import ImageField, IntegerField, ModelForm, ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class ProfileUpdateForm(forms.ModelForm):
    image = ImageField(
        label=""
    )
    template_name_p = "users/image_button.html"
    class Meta:
        model = Profile
        fields = ['image']

class ChoicesUpdateForm(ModelForm):
    player_1 = forms.ModelChoiceField(queryset=Player.objects.all().order_by('player_name'))
    player_2 = forms.ModelChoiceField(queryset=Player.objects.all().order_by('player_name'))
    player_3 = forms.ModelChoiceField(queryset=Player.objects.all().order_by('player_name'))
    predicted_score = IntegerField()

    class Meta:
        model = PlayerChoices
        fields = ['player_1', "player_2", "player_3", "predicted_score"]

    def clean(self):
        cleaned_data = self.cleaned_data

        player_1 = cleaned_data.get("player_1")
        player_2 = cleaned_data.get("player_2")
        player_3 = cleaned_data.get("player_3")
        predicted_score = cleaned_data.get("predicted_score")

        print(f"predicted score submitted :: {predicted_score}")

        odds_points_1 = Player.objects.get(player_name=player_1).odds_points
        odds_points_2 = Player.objects.get(player_name=player_2).odds_points
        odds_points_3 = Player.objects.get(player_name=player_3).odds_points
        total_points = odds_points_1 + odds_points_2 + odds_points_3

        if player_1 == player_2 or player_1 == player_3 or player_2 == player_3:
            raise ValidationError("Please choose three different players")
        
        if total_points < 150:
            print(f"{player_1} : {odds_points_1}")
            print(f"{player_2} : {odds_points_2}")
            print(f"{player_3} : {odds_points_3}")
            raise ValidationError(f"Combined points total must be at least 150 (Current Total Points: {total_points})")

        print(f"cleaned data is :: {cleaned_data}")

        return cleaned_data
        