from django.urls import path
from . import index


urlpatterns = [
    path('', index.postListView.as_view(), name='Home'),
    path('about/', index.about, name='About'),
    path('post/<int:pk>/', index.postDetailView, name='Post'),
    path('post/create/', index.postCreateView.as_view(), name='Create'),
    path('post/update/<int:pk>/', index.postUpdateView.as_view(), name='Update'),
    path('post/delete/<int:pk>/', index.postDeleteView.as_view(), name='Delete'),
    path('<str:username>/posts/', index.userPostListView.as_view(), name='User'),
]



