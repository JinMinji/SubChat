from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from freeapp.models import Post, Bookmark
from .models import Emoji
from accounts.forms import UserForm
from accounts.models import User
from .forms import CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime


def mypage(request):
    if request.method == "POST":
        #수정하기
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('/profile/mypage')

        else:
            print("폼 유효성 검사 실패")
            return redirect('/profile/mypage')

    # 로그인 사용자의 작성글 가져오기
    user_id = request.user.id
    my_post_list = Post.objects.all().order_by("-id").filter(author_id=user_id)

    # 로그인 사용자의 북마크한 글 가져오기
    my_bookmarks = Bookmark.objects.all().filter(user_id=user_id).values("post_id")
    post_id_list = list()
    for dic in my_bookmarks:
        post_id_list.append(dic["post_id"])

    all_post = Post.objects.all().order_by("-id")
    my_bookmark_list = list()
    for post in all_post:
        if post.id in post_id_list:
            my_bookmark_list.append(post)

    # 사용자 정보 form 가져오기
    form = UserForm(instance=request.user)

    try:
        my_emoji = Emoji.objects.get(id=request.user.emoji_id)
    except:
        my_emoji = Emoji.objects.get(id=1)

    emoji_list = Emoji.objects.all()
    return render(request, 'profileapp/mypage.html', {'form': form, 'my_emoji': my_emoji, 'my_post_list': my_post_list, 'my_bookmark_list': my_bookmark_list})


def emoji(request):
    emoji_list = Emoji.objects.all()
    if str(request.user) == 'AnonymousUser':
        return redirect('/accounts/login')

    try:
        my_emoji = Emoji.objects.get(id=request.user.emoji_id)
    except:
        my_emoji = Emoji.objects.get(id=1)
    return render(request, 'profileapp/emoji_select.html', {'emoji_list': emoji_list, "my_emoji": my_emoji})


def emoji_modify(request, new_emoji_id):
    user = User.objects.get(id=request.user.id)
    user.emoji_id = new_emoji_id
    user.save()

    return redirect('/profile/mypage')


def test(request):
    if request.method == "POST":
        # 수정하기
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        print(user_form)
        if user_form.is_valid():
            user_form.save()
            return redirect('/profile/mypage')

        else:
            messages.warning(request, "입력값 형식 오류, 수정할 내용을 확인해주세요.")
            return redirect('/profile/mypage')

    # 로그인 사용자의 작성글 가져오기
    user_id = request.user.id
    my_post_list = Post.objects.all().filter(author_id=user_id)

    # 로그인 사용자의 북마크한 글 가져오기
    my_bookmarks = Bookmark.objects.all().filter(user_id=user_id).values("post_id")
    post_id_list = list()
    for dic in my_bookmarks:
        post_id_list.append(dic["post_id"])
    all_post = Post.objects.all()
    my_bookmark_list = list()
    for post in all_post:
        if post.id in post_id_list:
            my_bookmark_list.append(post)

    # 사용자 정보 form 가져오기
    form = UserForm(instance=request.user)

    try:
        my_emoji = Emoji.objects.get(id=request.user.emoji_id)
    except:
        my_emoji = Emoji.objects.get(id=1)

    emoji_list = Emoji.objects.all()
    return render(request, 'profileapp/mypage.html', {'form': form, 'my_emoji': my_emoji, 'my_post_list': my_post_list,
                                                      'my_bookmark_list': my_bookmark_list})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return render(request, 'profileapp/change_complete.html')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'profileapp/change_password.html', {'form': form})

