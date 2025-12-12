from rest_framework import  viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action 
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer 
from django.contrib.auth.models import User
from django.utils import timezone

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = Book.objects.all()


    def get_queryset(self):
      queryset = Book.objects.all()
      available = self.request.query_params.get('available')
      title = self.request.query_params.get('title')
      author = self.request.query_params.get('author')
      isbn = self.request.query_params.get('isbn')

      if available == 'true':
         queryset = queryset.filter(available_copies__gt=0)
      if title:
         queryset = queryset.filter(title_icontains=title)
      if author:
         queryset = queryset.filter(author_icontains=author)
      if isbn:
         queryset = queryset.filter(isbn=isbn)
      return queryset

    # custom actions for checkout
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
       book = self.get_object() 
       user = request.user

       if book.available_copies < 1:
          return Response({"error": "Book not available"}, status=status.HTTP_400_BAD_REQUEST)   
 
       if Transaction.objects.filter(user=user, book=book, transaction_type='checkout', return_date_isnull=True).exists():
          return Response({"error": "You already checked out this book"}, status=status.HTTP_400_BAD_REQUEST)
       

       #create transaction
       Transaction.objects.create(user=user, book=book, transaction_type='checkout', checkout_date=timezone.now())
       book.available_copies -= 1
       book.save()

       return Response({"success":f"Book '{book.title}' checked out successfully"})
    
     # Custom action for return
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        user = request.user

        try:
            transaction = Transaction.objects.get(user=user, book=book, transaction_type='checkout', return_date__isnull=True)
        except Transaction.DoesNotExist:
            return Response({"error": "You don't have this book checked out"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.transaction_type = 'return'
        transaction.return_date = timezone.now()
        transaction.save()

        book.available_copies += 1
        book.save()

        return Response({"success": f"Book '{book.title}' returned successfully"})