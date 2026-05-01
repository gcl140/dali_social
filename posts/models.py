from django.db import models
from members.models import Member

class Post(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('link', 'Link'),
    ]
    
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Member, through='Like', related_name='liked_posts')
    
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return f"{self.author.name}: {self.content[:50]}..."
    
    class Meta:
        ordering = ['-created_at']

class Like(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['member', 'post']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']