from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Post, Comment, Bookmark, Report, Like, Hate
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages

# Create your views here.


class PostList(ListView):
    model = Post
    paginate_by = 10    # 페이지 나누는 부분

    def get_queryset(self):
        all_post = Post.objects.all().order_by("-id")
        if self.kwargs['line_num'] == 0:
            return all_post

        try:
            line_post = all_post.filter(line=self.kwargs['line_num'])
        except:
            return all_post

        search_keyword = self.request.GET.get("searchword")

        if search_keyword:
            if len(search_keyword) > 1:
                searched_list = line_post.filter(Q(title__icontains=search_keyword) | Q(contents__icontains=search_keyword))
                return searched_list

            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')

        return line_post

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
            return redirect("free:post", pk)

    post = Post.objects.get(id=pk)
    post.view_cnt += 1
    post.save()
    qs = Comment.objects.all()
    comments = qs.filter(Q(post_id=pk))
    bookmarks = Bookmark.objects.all()
    tmp = bookmarks.filter(post_id=pk, user_id=request.user.id)
    bookmark = False
    if tmp:
        bookmark = True

    return render(request, 'freeapp/post_read.html', {'post': post, 'comment_list': comments, 'bookmark': bookmark})


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
        form = PostForm(instance=original_post)
        # print(form.title, form.contents)

    return render(request, 'freeapp/modify.html', {'form': form})


def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/free/list')


def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    tmp_post_id = comment.post_id
    comment.delete()
    return redirect('free:post', tmp_post_id)


def list(request):
    return redirect('free:list', 0)


def bookmark(request, pk):
    bookmarks = Bookmark.objects.all()
    tmp = bookmarks.filter(post_id=pk, user_id=request.user.id)
    if tmp:
        tmp.delete()
    else:
        new_bookmark = Bookmark()
        new_bookmark.post_id = pk
        new_bookmark.user_id = request.user.id
        new_bookmark.save()

    return redirect('free:post', pk)


def report(request, pk):
    reported_post = Post.objects.get(id=pk)
    if request.method == "POST":
        report = Report.objects.all()
        tmp = report.filter(post_id=pk, user_id=request.user.id)
        if tmp:
            messages.error(request, "이미 신고 완료한 게시글입니다.")
            return render(request, 'freeapp/report_unable.html')

        else:
            #신고 객체 추가
            new_report = Report()
            new_report.post_id = pk
            new_report.user_id = request.user.id
            new_report.save()
            # 신고 대상 포스트의 신고건수 + 1
            reported_post.report_cnt += 1
            reported_post.save()
            messages.warning(request, "신고가 완료되었습니다.")

        return render(request, 'freeapp/report_close.html')

    else:
        return render(request, 'freeapp/report.html', {'post': reported_post})


def like(request, pk):
    all_like = Like.objects.all()
    like = all_like.filter(post_id=pk, user_id=request.user.id)

    if like:    #이미 좋아요 함.
        return redirect('free:post', pk)

    else:   # 좋아요를 증가하기 전, 싫어요가 있는지 확인하고 삭제.
        all_hate = Hate.objects.all()
        hate = all_hate.filter(post_id=pk, user_id=request.user.id)
        if hate:
            hate.delete()

        new_like = Like()
        new_like.post_id = pk
        new_like.user_id = request.user.id
        new_like.save()
        return redirect('free:post', pk)


def hate(request, pk):
    all_hate = Hate.objects.all()
    hate = all_hate.filter(post_id=pk, user_id=request.user.id)

    if hate:  # 이미 싫어요 함. -> 변경없이 리턴
        return redirect('free:post', pk)

    else:  # 싫어요를 증가하기 전, 좋아요가 있는지 확인하고 있으면 삭제.
        all_like = Like.objects.all()
        like = all_like.filter(post_id=pk, user_id=request.user.id)
        if like:
            like.delete()

        new_hate = Hate()
        new_hate.post_id = pk
        new_hate.user_id = request.user.id
        new_hate.save()

        return redirect('free:post', pk)

