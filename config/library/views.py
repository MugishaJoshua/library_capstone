from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Transaction
from .serializers import BookSerializer
from django.utils import timezone
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer  # ✅ Corrected

    def get_queryset(self):
        queryset = Book.objects.all()
        available = self.request.query_params.get('available')
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        isbn = self.request.query_params.get('isbn')

        if available == 'true':
            queryset = queryset.filter(available_copies__gt=0)
        if title:
            queryset = queryset.filter(title__icontains=title)  # ✅ Fixed
        if author:
            queryset = queryset.filter(author__icontains=author)  # ✅ Fixed
        if isbn:
            queryset = queryset.filter(isbn=isbn)
        return queryset

    # Custom action for checkout
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        book = self.get_object()
        user = request.user

        if book.available_copies < 1:
            return Response({"error": "Book not available"}, status=status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(user=user, book=book, transaction_type='checkout', return_date__isnull=True).exists():
            return Response({"error": "You already checked out this book"}, status=status.HTTP_400_BAD_REQUEST)

        # Create transaction
        Transaction.objects.create(user=user, book=book, transaction_type='checkout', checkout_date=timezone.now())
        book.available_copies -= 1
        book.save()

        return Response({"success": f"Book '{book.title}' checked out successfully"})

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


# Registration endpoint
class RegisterUser(APIView):
    permission_classes = []  # Anyone can register

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "username": user.username})