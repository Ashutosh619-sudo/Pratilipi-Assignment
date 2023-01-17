from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','password','username')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User(email=validated_data.get("email",""),first_name=validated_data.get("first_name",""),last_name=validated_data.get("last_name",""),username=validated_data.get("username"))
        user.set_password(validated_data["password"])
        user.save()
        return user