from django.contrib import admin
from .models import Post, Category, Comment, SiteInfo
from django_summernote.admin import SummernoteModelAdmin


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'site_name', 'site_url']
    list_display_links = ['site_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'is_publish_ok','is_comment_ok']
    list_display_links = ['category_name']
    list_editable = ['is_publish_ok', 'is_comment_ok']

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    #summernote_fields = '__all__' #('content',)
    summernote_fields = ('content',)
    list_display=['id','category','title','is_publish_ok','created_at','updated_at']
    list_display_links = ['title']
    list_filter = ['category','title','is_publish_ok']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_publish_ok']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post_content_len']

    # list_select_related = ['post']

    def post_content_len(self, comment):
        return '{}글자'.format(len(comment.post.content))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('post')