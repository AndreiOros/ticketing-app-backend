from rest_framework import serializers
from .models import Board, List, Card
from user.models import CustomUser


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'list']
        read_only_fields = ['id', 'created_at']


class ListSerializer(serializers.ModelSerializer):
    board = serializers.StringRelatedField()
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'title', 'created_at', 'board', 'cards']
        read_only_fields = ['id', 'created_at']

class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all()
    )
    lists = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'owner', 'members', 'lists']
        read_only_fields = ['id', 'created_at', 'owner']