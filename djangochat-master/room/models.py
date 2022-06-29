from concurrent.futures.process import _MAX_WINDOWS_WORKERS
from django.db import models


class Room(models.Model):
    bot_id = models.CharField(max_length=50, default="None")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    wellcome_msg = models.CharField(
        max_length=510, default="Hi, welcome to this chatbot")
    Questions = models.TextField()
    Answers = models.TextField()

    def __str__(self):
        return self.name


class Chat (models.Model):
    chat_room = models.CharField(max_length=100)
    message = models.CharField(max_length=50)
    message_from = models.CharField(max_length=100, default='bot')
