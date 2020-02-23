from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    def items(self):
        return Post.objects.filter(is_publish_ok=True).order_by('created_at')
    def lastmod(self, obj):
        return obj.updated_at
