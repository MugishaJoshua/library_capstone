from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title= models.CharField(max_length=255)
    author= models.CharField(max_length=255)
    isbn= models.CharField(max_length=13, unique=True)
    published_date= models.DateField(null=True, blank=True)
    total_copies= models.PositiveIntegerField(default=1)
    available_copies= models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.author}"
    

class Transaction(models.Model):
    CHECKOUT ='checkout'
    RETURN = 'return'
    TRANSACTIONAL_TYPES = [
        (CHECKOUT, 'checkout'),
        (RETURN, 'return')
    ]    

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTIONAL_TYPES)
    checkout_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.book.title}"
