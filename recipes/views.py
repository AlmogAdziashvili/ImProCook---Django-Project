from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RecipeModelForm, CommentModelForm
from .models import Recipe, Like, Comment
from accounts.models import MyUser, Follow
from django.utils.timezone import utc
import datetime
import itertools
import operator


def most_common(L):
    SL = sorted((x, i) for i, x in enumerate(L))
    groups = itertools.groupby(SL, key=operator.itemgetter(0))

    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        return count, -min_index

    return max(groups, key=_auxfun)[0]


def home_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        feed = list(Recipe.objects.filter(user_pk=request.user.pk)) + list(
            Follow.objects.filter(user_pk=request.user.pk)) + list(
            Follow.objects.filter(following_pk=request.user.pk)) + list(Like.objects.filter(user_pk=request.user.pk))
        for f in Follow.objects.filter(user_pk=request.user.pk):
            feed = feed + list(Recipe.objects.filter(user_pk=f.following_pk)) + list(
                Like.objects.filter(user_pk=f.following_pk))
        feed.sort(key=lambda r: r.create_time, reverse=True)
        posts = []
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        for p in feed:
            time_passed = int((now - p.create_time).total_seconds() / 3600)
            if time_passed > 24:
                time_passed = str(int(time_passed / 24)) + " days ago"
            else:
                time_passed = str(time_passed) + " hours ago"
            if type(p) is Recipe:
                if p.user_pk is request.user.pk:
                    posts.append(['mr', request.user.profile_pic.url, p.pk, p.recipe_pic.url, p.title, time_passed])
                else:
                    posts.append(
                        ['r', MyUser.objects.get(id=p.user_pk).profile_pic.url, p.id, p.recipe_pic.url, p.title,
                         MyUser.objects.get(id=p.user_pk).first_name + " " + MyUser.objects.get(id=p.user_pk).last_name,
                         p.user_pk, time_passed])
            elif type(p) is Follow:
                if p.user_pk is request.user.pk:
                    posts.append(['mf', request.user.profile_pic.url,
                                  MyUser.objects.get(id=p.following_pk).first_name + " " + MyUser.objects.get(
                                      id=p.following_pk).last_name, p.following_pk, time_passed])
                else:
                    posts.append(['f', MyUser.objects.get(id=p.user_pk).profile_pic.url,
                                  MyUser.objects.get(id=p.user_pk).first_name + " " + MyUser.objects.get(
                                      id=p.user_pk).last_name, p.user_pk, time_passed])
            else:
                if p.user_pk is request.user.pk:
                    posts.append(['ml', time_passed, request.user.profile_pic.url, p.recipe_pk,
                                  Recipe.objects.get(id=p.recipe_pk).recipe_pic.url,
                                  Recipe.objects.get(id=p.recipe_pk).title])
                else:
                    posts.append(['l', time_passed, MyUser.objects.get(id=p.user_pk).profile_pic.url, p.user_pk,
                                  MyUser.objects.get(id=p.user_pk).first_name + " " + MyUser.objects.get(
                                      id=p.user_pk).last_name, p.recipe_pk,
                                  Recipe.objects.get(id=p.recipe_pk).recipe_pic.url, Recipe.objects.get(
                            id=p.recipe_pk).title])  # MyUser.objects.get(id=p.user_pk).profile_pic.url, p.id, p.recipe_pic.url, p.title, MyUser.objects.get(id=p.user_pk).first_name + " " + MyUser.objects.get(id=p.user_pk).last_name, p.user_pk, time_passed])

    return render(request, "recipes/home.html", {"posts": posts})


def recipe_creation_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        form = RecipeModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_pk = request.user.pk
            obj.save()
            return HttpResponseRedirect('/')

    return render(request, "recipes/recipe_creation.html", {"form": form})


def top_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        x = []
        for l in Like.objects.all():
            x.append(l.recipe_pk)
        x = most_common(x)

    return HttpResponseRedirect('/recipes/' + str(x))


def favorite_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        recipe_list = []
        for obj in Like.objects.filter(user_pk=request.user.pk):
            recipe_list.append(Recipe.objects.get(id=obj.recipe_pk))
    return render(request, "recipes/favorite.html", {"recipe_list_": recipe_list})


def recipe_view(request, pk, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        liked = False
        comments = []
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        for c in Comment.objects.filter(recipe_pk=pk):
            time_passed = int((now - c.create_time).total_seconds() / 3600)
            if time_passed > 24:
                time_passed = str(int(time_passed / 24)) + " days ago"
            else:
                time_passed = str(time_passed) + " hours ago"
            user = MyUser.objects.get(id=c.user_pk)
            comments.append(
                [user.first_name + " " + user.last_name, user.profile_pic.url, c.content, time_passed, c.user_pk])
        if Like.objects.filter(user_pk=request.user.pk, recipe_pk=pk).exists():
            liked = True
        if request.GET.get('like'):
            l = Like(user_pk=request.user.pk, recipe_pk=pk)
            l.save()
            return HttpResponseRedirect('/recipes/' + str(pk))
        if request.GET.get('unlike'):
            Like.objects.filter(user_pk=request.user.pk, recipe_pk=pk).delete()
            return HttpResponseRedirect('/recipes/' + str(pk))
        form = CommentModelForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_pk = request.user.pk
            obj.recipe_pk = pk
            obj.save()
            return HttpResponseRedirect('/recipes/' + str(pk))

        return render(request, "recipes/recipe_view.html", {"recipe": Recipe.objects.get(id=pk),
                                                            "instructions": Recipe.objects.get(
                                                                id=pk).instructions.splitlines(),
                                                            "ingredients": Recipe.objects.get(
                                                                id=pk).ingredients.splitlines(),
                                                            "name": MyUser.objects.get(id=Recipe.objects.get(
                                                                id=pk).user_pk).first_name + " " + MyUser.objects.get(
                                                                id=Recipe.objects.get(id=pk).user_pk).last_name,
                                                            "liked": liked,
                                                            "like_count": Like.objects.filter(recipe_pk=pk).count(),
                                                            "form": form,
                                                            "comments": comments})


def search_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    else:
        if request.method == "POST":
            query = request.POST['search_query']
            recipes = Recipe.objects.filter(title__contains=query)
            accounts = list(MyUser.objects.filter(first_name__contains=query)) + list(MyUser.objects.filter(last_name__contains=query))
            return render(request, "recipes/search.html", {"q": query,
                                                           "recipes": recipes,
                                                           "recipes_count": recipes.count(),
                                                           "accounts": set(accounts),
                                                           "accounts_count": len(set(accounts))})
        else:
            return HttpResponseRedirect('/')

