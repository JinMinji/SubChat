from django.urls import path
from . import views

app_name = 'free'

urlpatterns = [
    # path('list/<int:line_num>', views.PostList.as_view(), name="list"),
    path('list/', views.PostList.as_view(), name="list"),
    path('post/<int:pk>', views.post, name="post"),
    path('create/', views.create, name="create"),
    path('modify/<int:pk>', views.modify, name="modify"),
    path('delete/', views.delete, name="delete"),
]