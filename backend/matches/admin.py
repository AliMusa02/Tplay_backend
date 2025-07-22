from django.contrib import admin
from .models import Invitation, Matches
# Register your models here.


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender_team', 'receiver_team', 'venue', 'time_slot', 'date', 'status'
                    'created_at', 'about', 'captain')
    list_filter = ('status', 'venue')
    ordering = ('created_at',)


@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'is_played',
                    'venue', 'time_slot', 'created_at')
    list_filter = ('is_played', 'venue')
