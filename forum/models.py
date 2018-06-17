from django.db import models
from django.utils import timezone

# Create your models here.


class Thread(models.Model):
    category_name = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    last_activity_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    posting_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "In \"" + str(self.thread.title) + "\" by " + str(self.author) + " - " + str(self.posting_date)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    posting_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "In \"" + str(self.post.thread.title) + "\" comment by " + str(self.author) + " - " + str(self.posting_date)