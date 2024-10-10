from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status  # Add this line
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item, Comment
from .serializers import ItemSerializer, CommentSerializer
from django.http import HttpResponse
from django.db.models import Q  # Import Q for complex queries

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the task manager home!")

# List and create item 
class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]  # DRF auth
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Filter backend
    filterset_fields = ['status', 'priority', 'due_date', 'assigned_to']  # Fields to filter with
    search_fields = ['title', 'description']  # Fields to search with (corrected here)

    # Optionally, you can customize the queryset for searching
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | Q(description__icontains=search_term)
            )
        return queryset

# Retrieve, update, and delete
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:

            # Call the original create method
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # Return the serialized data of the created comment
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error creating comment:", e)  # Optional logging
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)