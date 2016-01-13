from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

def posts_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def posts_show(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'posts/show.html', {'post': post})

def posts_create(request):
    form = PostForm()

    if(request.method == 'POST'):
        form = PostForm(request.POST)
    
        if(form.is_valid()):
            post = form.save(commit=False)    
            post.save()

            messages.success(request, 'Successfully created!')
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            messages.success(request, 'Please correct your errors.')

    return render(request, 'posts/_form.html', {'form': form, 'submitButtonText': 'Create Post'})

def posts_update(request, id):
    post = get_object_or_404(Post, pk=id)
    form = PostForm(instance=post)

    if(request.method == 'POST'):
        form = PostForm(request.POST, instance=post)
    
        if(form.is_valid()):
            post = form.save(commit=False)    
            post.save()

            messages.success(request, 'Successfully updated!')
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            messages.success(request, 'Please correct your errors.')

    return render(request, 'posts/_form.html', {'form': form, 'submitButtonText': 'Update Post'})

def posts_delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    messages.success(request, 'Successfully deleted!')
    return redirect('posts:index')