from django.urls import path
from .views import ItemList, ItemDetail,home,CommentList

urlpatterns=[
    path('',home,name='home'),
    path('items/', ItemList.as_view(), name='item-list'),# For listing and creating items
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),  # For retrieving, updating, and deleting items
    path('comments/',CommentList.as_view(),name='comment-list'),
]