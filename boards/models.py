from django.db import models

# Create your models here.


import math
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.text import Truncator 
from markdown import markdown
from django.shortcuts import get_object_or_404
from django.http import Http404

class BoardType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

    def to_json(self):
        json_BoardType = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return json_BoardType

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    type = models.ForeignKey(BoardType, related_name='boards',on_delete=models.CASCADE,null=True)
    growth=models.DecimalField(max_digits=10, decimal_places=2,null=True)  

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()
    
    def to_json(self):
        json_board = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return json_board


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.subject
    
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)
    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6
    
    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)
    
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

    
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.DO_NOTHING)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
    
    

