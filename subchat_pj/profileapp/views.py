from django.shortcuts import render, redirect

# Create your views here.
from freeapp.models import Post, Bookmark
from .models import Emoji
from accounts.forms import UserForm
from accounts.models import User


def mypage(request):
    if request.method == "POST":
        #수정하기
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
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
    return render(request, 'profileapp/mypage_bak.html', {'form': form, 'my_emoji': my_emoji, 'my_post_list': my_post_list,
                                                      'my_bookmark_list': my_bookmark_list})

