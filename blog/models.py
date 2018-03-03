import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=14)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=40)
    excerpt = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    created_time = models.DateField()
    modified_time = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_time']
    
    def update_view(self):
        self.views+=1
        self.save(update_fields=['views'])
    
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
            self.excerpt = strip_tags(md.convert(self.body))[:250] + '...'
        super(Post, self).save(*args, **kwargs)