from rest_framework import serializers
from .models import Content
# remember to import the File model

class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = "__all__"
        read_only_fields = ('user_id','likes')