from django.db import models

# Create your models here.
class Content(models.Model):

    title = models.CharField(max_length=1000,null=False)
    story = models.TextField(null=False)
    date_published = models.DateField()
    user_id = models.IntegerField(null=False)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title