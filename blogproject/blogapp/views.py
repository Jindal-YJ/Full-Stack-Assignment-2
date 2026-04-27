from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .models import Post
from .forms import PostForm
from .forms import UserRegistrationForm


# Home Page
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            posts = Post.objects.all().order_by('-created_at')
        else:   # Normal User
            posts = Post.objects.filter(author=request.user).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'blogapp/home.html', {'posts': posts})


# Signup Page
def signup(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})


# Create Post Page
@login_required
def create_post(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Post created successfully!")
            return redirect('home')

    else:
        form = PostForm()

    return render(request, 'blogapp/create_post.html', {'form': form})


# Post Detail Page
def post_details(request, id):

    post = get_object_or_404(Post, id=id)

    return render(request, 'blogapp/post_detail.html', {'post': post})