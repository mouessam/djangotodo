from django.contrib.auth.models import User
from drf_yasg import openapi
from rest_framework import serializers

from todolist.models import TodoList


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        password = validated_data.pop('password')
        user.set_password(password)
        user.save()
        return user


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ('id', 'title', 'content', 'created', 'completed', 'due_date', 'owner')
        extra_kwargs = {'owner': {'write_only': True}, 'id': {'read_only': True}}
        swagger_schema_fields = {
            "title": openapi.TYPE_STRING,
            "content": openapi.TYPE_STRING,
            "created": openapi.FORMAT_DATE,
            "completed": openapi.TYPE_BOOLEAN,
            "due_date": openapi.FORMAT_DATE,
            "required": ["title"],
        }
