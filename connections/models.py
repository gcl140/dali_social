from django.db import models
from members.models import Member

class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    from_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sent_connections')
    to_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['from_member', 'to_member']
        ordering = ['-created_at']