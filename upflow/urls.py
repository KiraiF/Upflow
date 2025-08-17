"""
URL configuration for upflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from core import views
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('vote/<int:post_id>/<str:direction>/', views.vote_post, name='vote_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('u/<str:username>/', views.profile_view, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('post/new/', views.create_post, name='create_post'),
    path('communities/', views.communities, name='communities'),
    path('communities/r/<str:community>', views.communities, name='communities'),
    path('accounts/', include('allauth.urls')),  
    path('create_community/', views.create_community, name="create_community"),
    path('post/<int:post_id>/', views.post_view, name='post_view'),
    path('comment/<int:post_id>',views.comment_create, name="create_comment"),
]
