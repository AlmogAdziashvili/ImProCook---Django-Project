from django.shortcuts import render
from .forms import UserCreationForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, get_user_model, logout
from .models import Follow
from recipes.models import Recipe

User = get_user_model()


def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    return render(request, "accounts/register.html", {"form": form})


def login_view(request, *args, **kwargs):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email_ = form.cleaned_data.get("email")
        user_obj = User.objects.get(email=email_)
        login(request, user_obj)
        return HttpResponseRedirect('/')
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        logout(request)
        return HttpResponseRedirect("/login")


def profile_view(request, pk, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        recipes = Recipe.objects.filter(user_pk=pk)
        profile_stat = 0
        if Follow.objects.filter(user_pk=request.user.pk, following_pk=pk).exists():
            profile_stat = 1
        elif str(pk) == str(request.user.pk):
            profile_stat = 2
        followers_count = Follow.objects.filter(following_pk=pk).count()
        following_count = Follow.objects.filter(user_pk=pk).count()
        user_obj = User.objects.get(id=pk)
        if request.GET.get('follow'):
            f = Follow(user_pk=request.user.pk, following_pk=pk)
            f.save()
            return HttpResponseRedirect('/profile/' + str(pk))
        if request.GET.get('unfollow'):
            Follow.objects.filter(user_pk=request.user.pk, following_pk=pk).delete()
            return HttpResponseRedirect('/profile/' + str(pk))
        return render(request, "accounts/profile.html",
                      {"user_": user_obj, "profile_stat_": profile_stat, "followers_count_": followers_count,
                       "following_count_": following_count,
                       "recipes": recipes})


def followers_view(request, pk, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        usr_list = []
        fol_list = Follow.objects.filter(following_pk=pk)
        for fol in fol_list:
            usr_list.append(User.objects.get(pk=fol.user_pk))
        return render(request, "accounts/followers.html", {"list_": usr_list,})


def following_view(request, pk, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        usr_list = []
        fol_list = Follow.objects.filter(user_pk=pk)
        for fol in fol_list:
            usr_list.append(User.objects.get(pk=fol.following_pk))
        return render(request, "accounts/following.html", {"list_": usr_list,})
