from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap


sitemaps = {
    'posts':PostSitemap,
}


app_name = 'blog'
urlpatterns = [
    path('', views.post_index, name='post_index'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('.well-known/pki-validation/0951996431BB19E15491559D4B5A3F68.txt', TemplateView.as_view(template_name="0951996431BB19E15491559D4B5A3F68.txt", content_type="text/plain"), name="project_ssl_file"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="project_robots_file"),
    path('<int:pk>/<str:slug>/', views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.post_list, name='post_list'),
    path('search/', views.search_post_list, name='post_search'),
    path('tag/<str:tag>/', views.tag_post_list, name='tag_post_list'),
    path('autowrite/', views.auto_write, name='auto_write'),
]
