from django.db import models

# Create your models here.

class Interaction(models.Model):
    user_id = models.CharField(max_length=255)
    content_id = models.CharField(max_length=255)
    INTERACTION_TYPE_CHOICES = (
        ('like', 'Like'),
        ('read', 'Read'),
    )
    interaction_type = models.CharField(max_length=255, choices=INTERACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id','content_id', 'interaction_type')

    def __str__(self):
        return f'{self.user_id} {self.interaction_type} {self.content_id}'