from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import PlayerChoices, Player, ESPN

from .forms import UserRegisterForm, ProfileUpdateForm, ChoicesUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required

def profile(request):
#    player = Player.objects.all().order_by("odds_points")
    espn = ESPN.objects.all().order_by("row_num").values()
    if request.method == 'POST':
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        # choices_form = ChoicesUpdateForm(request.POST)

        # if p_form.is_valid() and choices_form.is_valid():
        #     p_form.save()

        #     choices = choices_form.save(commit=False)
        #     PlayerChoices.objects.update_or_create(
        #         user_id=request.user.id,
        #         defaults={
        #             'player_1': choices.player_1,
        #             'player_2': choices.player_2,
        #             'player_3': choices.player_3,
        #             'predicted_score': choices.predicted_score
        #         }
        #     )
        #     messages.success(request, 'Your account has been updated')
        #     return redirect('profile')
        if p_form.is_valid():
            p_form.save()
            # choices_form = ChoicesUpdateForm(initial={
            #     'player_1': player_choices.player_1,
            #     'player_2': player_choices.player_2,
            #     'player_3': player_choices.player_3,
            #     'predicted_score': player_choices.predicted_score
            # }
            return redirect('profile')
    else:
        try:
            player_choices = PlayerChoices.objects.get(user_id=request.user.id)
            choices_form = ChoicesUpdateForm(
                initial={
                    'player_1': player_choices.player_1,
                    'player_2': player_choices.player_2,
                    'player_3': player_choices.player_3,
                    'predicted_score': player_choices.predicted_score
                }
            )
        except Exception as e:
            choices_form = ChoicesUpdateForm(initial={
                'player_1': PlayerChoices._meta.get_field('player_1').get_default(),
                'player_2': PlayerChoices._meta.get_field('player_2').get_default(),
                'player_3': PlayerChoices._meta.get_field('player_3').get_default(),
                'predicted_score': PlayerChoices._meta.get_field('predicted_score').get_default()
                }
            )

        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "p_form": p_form,
        "choices_form": choices_form,
#        "player": player,
        "espn": espn,
        "player_choices": player_choices
    }
    return render(request, 'users/profile.html', context)
