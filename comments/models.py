from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('blog.post', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]