from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Yard, Profile, CommentYard, ReplyToYardComment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
"""
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
"""
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class YardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yard
        fields = "__all__"

class CommentYardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentYard
        fields = "__all__"

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToYardComment
        fields = "__all__"