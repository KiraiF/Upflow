from django.shortcuts import render , redirect, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-created_at')  # show latest posts first
    return render(request, 'core/home.html', {'posts': posts})
def upvote_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        post.karma += 1
        post.save()
    return redirect('home')
def downvote_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        post.karma -= 1
        post.save()
    return redirect('home')
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    context= {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'core/profile.html', context)