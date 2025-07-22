from django.contrib import admin
from .models import Posts
# Register your models here.


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content',
                    'post_pic', 'created_at')
    search_fields = ('author')
    ordering = ('created_at')



# @admin.register(TeamMember)
# class VenueSlotsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'team', 'joined_at', 'role')
#     list_filter = ('team', 'user')
