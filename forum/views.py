from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from .forms import *


def index(request):
    threadlist = Thread.objects.all()
    categories = []
    for thread in threadlist:
        if thread.category_name not in categories:
            categories.append(thread.category_name)
    cat1 = []
    cat2 = []
    for i in range(len(categories)):
        if i % 2 == 0:
            cat1.append(categories[i])
        else:
            cat2.append(categories[i])
    if len(cat1) > len(cat2):
        cat2.append("")
    context = {'categories': zip(cat1, cat2)}
    return render(request, 'forum/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = MySignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('forum:index')
    else:
        form = MySignUpForm()
    return render(request, 'forum/signup.html', {'form': form})


def add_thread(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ThreadForm(request.POST)
            if form.is_valid():
                notsaved = form.save(commit=False)
                notsaved.author = request.user
                notsaved.save()
                return redirect('forum:thread_details', category=notsaved.category_name, threadID=notsaved.pk)
        else:
            form = ThreadForm()
        return render(request, 'forum/add_thread.html', {'form': form})
    else:
        return redirect('forum:login')


def threadlist(request, category):
    threads = get_list_or_404(Thread, category_name=category)
    context = {'threads': threads, 'category': category}
    return render(request, 'forum/threadlist.html', context)


def thread_details(request, category, threadID):
    thread = get_object_or_404(Thread, pk=threadID)
    context = {'thread': thread, 'category': category}
    return render(request, 'forum/thread_details.html', context)


def see_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        if request.user == user:
            context = {'user': user}
            return render(request, 'forum/see_profile.html', context)
    return redirect('forum:login')


def answer(request, category, threadID):
    thread = get_object_or_404(Thread, pk=threadID)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                notsaved = form.save(commit=False)
                thread.last_activity_date = timezone.now()
                thread.save()
                notsaved.author = request.user
                notsaved.thread = thread
                notsaved.save()
                context = {'thread': thread, 'category': category, 'form': form}
                # return render(request, 'forum/thread_details.html', context)
                return redirect('forum:thread_details', threadID=threadID, category=category)
        else:
            form = PostForm()
        context = {'thread': thread, 'category': category, 'form': form, 'message': 'Add answer'}
        return render(request, 'forum/thread_details.html', context)
    else:
        return redirect('forum:login')


def profile_update(request, username):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['first_name']:
                    user.first_name = form.cleaned_data['first_name']
                if form.cleaned_data['last_name']:
                    user.last_name = form.cleaned_data['last_name']
                if form.cleaned_data.get('email'):
                    user.email = form.cleaned_data['email']
                user.save()
                return redirect('forum:see_profile', username=username)
        else:
            form = ProfileUpdateForm()
        return render(request, 'forum/profile_update.html', {'form': form})
    else:
        return redirect('forum:login')


def password_change(request, username):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=username)
        if request.user == user:
            if request.method == 'POST':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return redirect('forum:see_profile', username=username)
            else:
                form = PasswordChangeForm(request.user)
            return render(request, 'forum/password_change.html', {'form': form})
    return redirect('forum:login')


def user_delete(request, username):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=username)
        if request.user == user:
            user.delete()
            return redirect('forum:index')
    return redirect('forum:login')


def thread_delete(request, category, threadID):
    if request.user.is_authenticated:
        thread = get_object_or_404(Thread, pk=threadID)
        if request.user == thread.author:
            thread.delete()
            return redirect('forum:index')
        else:
            return redirect('forum:thread_details', category=category, threadID=threadID)
    else:
        return redirect('forum:login')


def post_delete(request, category, threadID, postID):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=postID)
        if request.user == post.author:
            post.delete()
        return redirect('forum:thread_details', category=category, threadID=threadID)
    else:
        return redirect('forum:login')
