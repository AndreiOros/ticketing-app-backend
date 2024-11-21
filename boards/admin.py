from django.contrib import admin
from .models import Board, List, Card, Comment

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'user__email')
    filter_horizontal = ('members',)

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'created_at')
    search_fields = ('name', 'board__name')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'due_date', 'created_at')
    search_fields = ('title', 'list__name')


@admin.register(Comment)
class CommnetAdmin(admin.ModelAdmin):
    list_display = ('text', 'card', 'author', 'created_at')
    search_fields = ('text', 'card__title', 'author__email')