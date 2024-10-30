from rest_framework import serializers
from .models import Board, List, Card
from user.models import CustomUser

class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'owner', 'members']
        read_only_fields = ['id', 'created_at', 'owner']

    def create(self, validated_data):
        owner = CustomUser.objects.get(id=self.context['request'].data['owner'])
        validated_data['owner'] = owner
        members = validated_data.pop('members')
        board = Board.objects.create(**validated_data)
        board.members.set(members)
        return board


class CardSerializer(serializers.ModelSerializer):
    list = serializers.StringRelatedField()

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