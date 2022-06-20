from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.db.models import Q

# Create your views here.

class PostList(ListView):
    model = Post
    paginate_by = 10    # 페이지 나누는 부분

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


def post(request, pk):  #게시글 내용 보여주는 곳
    if request.method == "POST":
        # 글쓰기
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)   #댓글 쓰는 부분
            comment.author = request.user
            comment.post_id = pk
            comment.save()
            print("test--------!")
            return redirect("free:post", pk)

    else:
        post = Post.objects.get(id=pk)
        post.view_cnt += 1
        post.save()
        qs = Comment.objects.all()
        comments = qs.filter(Q(post_id=pk))

    return render(request, 'freeapp/post_read.html', {'post': post, 'comment_list': comments})


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


def modify(request, pk):
    original_post = Post.objects.get(id=pk)
    original_post.last_update_date = timezone.now()

    if request.method == "POST":
        # 수정하기
        form = PostForm(request.POST, instance=original_post)
        if form.is_valid():
            if request.user == original_post.author:  # 글 작성자와 현재 사용자가 같을 때
                form.save()
                return redirect('/free/list')
    else:
        form = PostForm()
        # print(form.title, form.contents)

    return render(request, 'freeapp/modify.html', {'form': form, 'post': original_post})


def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/free/list')


def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    tmp_post_id = comment.post_id
    comment.delete()
    return redirect('free:post', tmp_post_id)