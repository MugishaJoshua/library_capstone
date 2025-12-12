from rest_framework import serializers
from .models import Book, Transaction
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
     class Meta:
          model = Book
          fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
     class Meta:
          model = Transaction
          fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'username', 'email']
          

