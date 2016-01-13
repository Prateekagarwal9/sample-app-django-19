from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

def index(request):
    posts_list = Post.objects.active()

    if request.user.is_staff or request.user.is_superuser:
        posts_list = Post.objects.all()

    query = request.GET.get('q')
    if(query):
        posts_list = posts_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(posts_list, 10) # Show 10 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/index.html', {'posts': posts, 'today': timezone.now()})

def show(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.draft and post.published_at > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    return render(request, 'posts/show.html', {'post': post, 'today': timezone.now()})

def create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm()

    if(request.method == 'POST'):
        form = PostForm(request.POST, request.FILES or None)
    
        if(form.is_valid()):
            post = form.save(commit=False)    
            post.user = request.user
            post.save()

            messages.success(request, 'Successfully created!')
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            messages.success(request, 'Please correct your errors.')

    return render(request, 'posts/_form.html', {'form': form, 'submitButtonText': 'Create Post'})

def update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)

    if(request.method == 'POST'):
        form = PostForm(request.POST, request.FILES or None, instance=post)
    
        if(form.is_valid()):
            post = form.save(commit=False)    
            post.save()

            messages.success(request, 'Successfully updated!')
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            messages.success(request, 'Please correct your errors.')

    return render(request, 'posts/_form.html', {'form': form, 'submitButtonText': 'Update Post'})

def delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Successfully deleted!')
    return redirect('posts:index')