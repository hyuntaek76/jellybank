from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_index, name='post_index'),
    path('<int:pk>/<str:slug>/', views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.post_list, name='post_list'),
    path('search/', views.search_post_list, name='post_search'),
    path('tag/<str:tag>/', views.tag_post_list, name='tag_post_list'),
    path('autowrite/', views.auto_write, name='auto_write'),
]