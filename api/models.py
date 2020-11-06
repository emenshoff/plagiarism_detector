from django.db import models

class Post(models.Model):
    date_stamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50 , null=False)
    content  = models.TextField()

    def __str__(self):
        return self.title

