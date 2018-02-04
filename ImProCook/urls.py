"""ImProCook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import profile_view, user_logout,register_view, login_view, followers_view, following_view
from recipes.views import home_view, recipe_creation_view, recipe_view,favorite_view, top_view, search_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view),
    url(r'^login/$', login_view),
    url(r'^register/$', register_view),
    url(r'^logout/$', user_logout),
    url(r'^share/$', recipe_creation_view),
    url(r'^profile/(?P<pk>[0-9]+)/$', profile_view),
    url(r'^followers/(?P<pk>[0-9]+)/$', followers_view),
    url(r'^following/(?P<pk>[0-9]+)/$', following_view),
    url(r'^recipes/(?P<pk>[0-9]+)/$', recipe_view),
    url(r'^favorite/$', favorite_view),
    url(r'^top/$', top_view),
    url(r'^search/$', search_view, name="search_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
