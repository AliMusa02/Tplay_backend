from django.contrib import admin
from .models import Teams, TeamMember
# Register your models here.


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_name', 'team_logo',
                    'created_at', 'about', 'captain')
    search_fields = ('team_name')
    ordering = ('created_at',)


@admin.register(TeamMember)
class TeamsMembersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'joined_at', 'role')
    list_filter = ('team', 'user')
