from django.shortcuts import render , redirect, get_object_or_404
from .models import Post, Community, Comment
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import CreatePostForm, CleanUserCreationForm,CreateCommunityForm
from django_ratelimit.decorators import ratelimit
from django.db import IntegrityError,transaction

def sentback(req):
    referer = req.META.get('HTTP_REFERER')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={req.get_host()}):
        return redirect(referer)
    return redirect('home')
def home(request):
    posts = Post.objects.all().order_by('-created_at')  # show latest posts first
    return render(request, 'core/home.html', {'posts': posts})
def vote_post(request, post_id, direction):  # direction is "up" or "down"
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to vote.")
            return redirect('home')

        post = get_object_or_404(Post, id=post_id)
        username = request.user.username
        post.vote(username, direction)
    return sentback(request)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        if request.user == post.user:
            post.delete()
            messages.success(request, "Post deleted successfully.")
        else:
            messages.error(request, "You are not allowed to delete this post.")
    return render(request, 'core/home.html')

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    context= {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'core/profile.html', context)
@ratelimit(key='user_or_ip', rate='15/m', block=True)
def login(request):
    if request.method == 'POST' and 'username' in request.POST:
        try:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                messages.success(request, f"Successfully signed in as {user.username}.")
            else:
                messages.error(request, "Invalid username or password.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect('home')
    else:
        login_form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'login_form': login_form})
@ratelimit(key='user_or_ip', rate='15/m', block=True)
def signup(request):
    if request.method == 'POST' and 'username' in request.POST:
        try:
            form = CleanUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)
                messages.success(request, f"Successfully signed up as {user.username}.")
            else:
                messages.error(request, "Please correct the errors below.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect('home')
    else:
        form = CleanUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)  
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('home')
    else:
        community = request.GET.get("community")  
        if community:
            form = CreatePostForm(initial={"community": community})
        else:
            form = CreatePostForm()
    return render(request, 'core/create_post.html', {'form': form})

def communities(request, community=None):
    if community is None:
        all_communities = Community.objects.all()
        single_community = None
        posts = None
        if not all_communities.exists():
            all_communities = []
    else:
        single_community = get_object_or_404(Community, name=community)
        all_communities = None
        posts = single_community.posts.all() 

    return render(request, 'core/communities.html', {
        'all_communities': all_communities,
        'single_community': single_community,
        'posts': posts
    })
def create_community(request):
    print(request.method)
    if request.method == 'POST':
        form = CreateCommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.owner = request.user 
            community.save()
            return redirect('communities')
    else:
        form = CreateCommunityForm()
    return render(request, 'core/create_community.html', {'form': form})
def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-commented_at')
    if request.method == "POST":
        return redirect('post_view', post_id=post.id)  
    return render(request, 'core/post_detail.html', {'post':post,'comments':comments})
@ratelimit(key='user_or_ip', rate='5/m', block=True)
def comment_create(request, post_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return sentback(request)

        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content", "").strip()

        if not content:
            messages.error(request, "Comment cannot be empty.")
            return sentback(request)

        _, created = Comment.objects.get_or_create(
            post=post,
            user=request.user,
            content=content
        )

        if created:
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "You cannot make duplicate comments.")

    return sentback(request)
