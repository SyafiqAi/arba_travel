from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
