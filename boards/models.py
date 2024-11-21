from django.db import models

# Create your models here.
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='boards')
    members = models.ManyToManyField('user.CustomUser', related_name='boards_member')


    def __str__(self):
        return self.name
    
    @property
    def all_lists(self):
        return self.lists.all()
    

class List(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title
    
    @property
    def all_cards(self):
        return self.cards.all()


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text