from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter = ('title', 'date', 'author')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)

