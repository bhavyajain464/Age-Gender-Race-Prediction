from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings

VISUAL_CHOICES = ( 
    ("1", "Image"), 
    ("2", "Video"), 
) 
# Create your models here.
class Visual(models.Model):
    name = models.CharField(max_length=250)
    visual_type = models.CharField(max_length=9,choices=VISUAL_CHOICES,default='1')
    upload_time = models.DateTimeField(default = timezone.now)
    visual = models.FileField(upload_to='original',default='logos/index.png')
    processes_visual = models.FileField(upload_to='converted',default='logos/index.png')

