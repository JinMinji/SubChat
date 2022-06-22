from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
from .models import Post

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)

admin.site.register(Post,PostAdmin)