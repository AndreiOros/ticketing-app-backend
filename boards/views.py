from rest_framework import viewsets
from .models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def perform_create(self, serializer):
        # Automatically set the board based on additional logic if needed
        serializer.save()


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        # Automatically set the list based on additional logic if needed
        serializer.save()