from django.db import models
from django.core.validators import URLValidator

class Member(models.Model):
    ROLE_CHOICES = [
        ('dev', 'Developer'),
        ('des', 'Designer'),
        ('pm', 'Project Manager'),
        ('core', 'Core Team'),
        ('mentor', 'Mentor'),
    ]
    
    YEAR_CHOICES = [
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('GR', 'Graduate'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default='2024')
    dev = models.BooleanField(default=False)
    des = models.BooleanField(default=False)
    pm = models.BooleanField(default=False)
    core = models.BooleanField(default=False)
    mentor = models.BooleanField(default=False)
    major = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    minor = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    birthday = models.CharField(max_length=5, blank=True, null=True, default='')  # Added null=True
    home = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    quote = models.TextField(blank=True, null=True, default='')  # Added null=True
    favorite_thing_1 = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    favorite_thing_2 = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    favorite_thing_3 = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    favorite_dartmouth_tradition = models.CharField(max_length=100, blank=True, null=True, default='')  # Added null=True
    fun_fact = models.TextField(blank=True, null=True, default='')  # Added null=True
    picture = models.URLField(blank=True, null=True, default='')  # Added null=True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_roles(self):
        roles = []
        if self.dev: roles.append('Developer')
        if self.des: roles.append('Designer')
        if self.pm: roles.append('Project Manager')
        if self.core: roles.append('Core Team')
        if self.mentor: roles.append('Mentor')
        return roles
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']