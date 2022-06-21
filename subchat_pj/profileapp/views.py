from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your views here.
from freeapp.models import Post, Bookmark


def mypage(request):
    my_user = request.user.id
    my_post_list = Post.objects.all().filter(author_id=my_user)

    my_bookmarks = Bookmark.objects.all().filter(user_id=my_user).values("post_id")

    post_id_list = list()
    for dic in my_bookmarks:
        post_id_list.append(dic["post_id"])

    all_post = Post.objects.all()
    my_bookmark_list = list()
    for post in all_post:
        if post.id in post_id_list:
            my_bookmark_list.append(post)

    return render(request, 'profile/mypage.html', {'my_post_list': my_post_list, 'my_bookmark_list': my_bookmark_list})
