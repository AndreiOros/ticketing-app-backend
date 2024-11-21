from rest_framework import serializers
from .models import Board, List, Card, Comment
from user.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), required=False)
    author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'card', 'author']
        read_only_fields = ['id', 'created_at']


class CardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    list = serializers.PrimaryKeyRelatedField(queryset=List.objects.all(), required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Card
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'list', 'position', 'comments']
        read_only_fields = ['id', 'created_at']


class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True)
    id = serializers.IntegerField(required=False)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), required=False)

    class Meta:
        model = List
        fields = ['id', 'title', 'created_at', 'board', 'cards']
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cards = representation.get('cards', [])
        ordered_cards = sorted(cards, key=lambda x: x['position'])
        representation['cards'] = ordered_cards
        return representation

class BoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    members = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'owner', 'members', 'lists']

    def create(self, validated_data):
        # Handle nested lists
        lists_data = validated_data.pop('lists', [])
        owner = validated_data.pop('owner')

        # Create the board
        board = Board.objects.create(owner=owner, **validated_data)

        # Add the owner to the members list
        board.members.add(owner)

        for list_data in lists_data:
            cards_data = list_data.pop('cards', [])
            list_instance = List.objects.create(board=board, **list_data)

            # Create cards for the new list
            for card_data in cards_data:
                Card.objects.create(list=list_instance, **card_data)

        return board

    def update(self, instance, validated_data):
        # Update the board fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Handle nested lists
        lists_data = validated_data.pop('lists', [])
        existing_lists = {list.id: list for list in instance.lists.all()}

        for list_data in lists_data:
            list_id = list_data.get('id')
            changed_card = []
            if list_id in existing_lists:
                list_instance = existing_lists.pop(list_id)
                list_instance.title = list_data.get('title', list_instance.title)
                list_instance.save()

                # Handle nested cards
                cards_data = list_data.get('cards', [])
                existing_cards = {card.id: card for card in list_instance.cards.all()}

                for card_data in cards_data:
                    card_id = card_data.get('id')
                    if card_id in existing_cards:
                        card_instance = existing_cards.pop(card_id)
                        card_instance.title = card_data.get('title', card_instance.title)
                        card_instance.description = card_data.get('description', card_instance.description)
                        card_instance.due_date = card_data.get('due_date', card_instance.due_date)
                        card_instance.position = card_data.get('position', card_instance.position)
                        card_instance.save()
                    elif card_id:
                        card_instance = Card.objects.get(id=card_id)
                        card_instance.title = card_data.get('title', card_instance.title)
                        card_instance.description = card_data.get('description', card_instance.description)
                        card_instance.due_date = card_data.get('due_date', card_instance.due_date)
                        card_instance.position = card_data.get('position', card_instance.position)
                        card_instance.list = list_instance
                        card_instance.save()
                    else:
                        # Create new cards
                        card_data.pop('list')
                        Card.objects.create(list=list_instance, **card_data)

                # Delete removed cards
                for card in existing_cards.values():
                    changed_card.append(card)
            else:
                # Create a new list
                cards_data = list_data.pop('cards', [])
                new_list_instance = List.objects.create(board=instance, **list_data)
    
                # Create new cards for the new list
                for card_data in cards_data:
                    Card.objects.create(list=new_list_instance, **card_data)

        # Delete removed lists
        for list_instance in existing_lists.values():
            list_instance.delete()

        return instance
