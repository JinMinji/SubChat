from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post
from .forms import PostForm
# Create your views here.

class PostList(ListView):
    model = Post


def post(request, pk):
    post = Post.objects.get(id=pk)
    post.view_cnt += 1
    post.save()
    return render(request, 'freeapp/post_read.html', {'post': post})


def create(request):
    if request.method == "POST":
        # 글쓰기
        form = PostForm(request.POST)
        if form.is_valid():
            form.author = request.user
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/free/list')
    else:
        form = PostForm()

    return render(request, 'freeapp/create.html', {'form': form})


def update(request):
    return


def delete(request):
    return

