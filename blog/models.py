from django.db import models

# Create your models here.
from django.urls import reverse
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.
class SiteInfo(models.Model):
    site_name = models.CharField(max_length=20, verbose_name='사이트명')
    site_url = models.CharField(blank=True, max_length=20, verbose_name='사이트주소')
    site_description = models.TextField(blank=True, max_length=50, verbose_name='사이트설명')
    site_photo = models.ImageField(blank=True, verbose_name='대표사진')
    site_script_01 = models.TextField(blank=True, max_length=200, verbose_name='첫번째 스크립트설치')
    site_script_02 = models.TextField(blank=True, max_length=200, verbose_name='두번째 스크립트설치')
    site_script_03 = models.TextField(blank=True, max_length=200, verbose_name='세번째 스크립트설치')

class Category(models.Model):
    COMMENT_STATUS_CHOICES = (
        (True, 'YES'),
        (False, 'NO'),
    )
    PUBLISH_STATUS_CHOICES = (
        (True, 'YES'),
        (False, 'NO'),
    )
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=20, verbose_name='카테고리명')
    photo = models.ImageField(blank=True, verbose_name='대표사진')
    #is_comment_ok = models.CharField(max_length=1,choices=COMMENT_STATUS_CHOICES, default='n', verbose_name='댓글공개')
    #is_publish_ok = models.CharField(max_length=1, choices=PUBLISH_STATUS_CHOICES, default='y', verbose_name='카테고리공개')
    is_comment_ok = models.BooleanField(choices=COMMENT_STATUS_CHOICES, default=True, verbose_name='댓글공개')
    is_publish_ok = models.BooleanField(choices=PUBLISH_STATUS_CHOICES, default=True, verbose_name='카테고리공개')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    PUBLISH_STATUS_CHOICES = (
        (True, '공개'),
        (False, '비공개'),
    )

    # user = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField(max_length=100, verbose_name='제목',
                             help_text='포스팅 제목을 입력해주세요. 최대 100자 내외.')
    slug = models.SlugField(allow_unicode='True', blank=True)
    content = models.TextField(verbose_name='내용')  # 길이 제한이 없는 문자열
    summary = models.TextField(max_length=150, blank=True, verbose_name='컨텐츠 요약')
    meta_keyword = models.CharField(max_length=100, blank=True, verbose_name='대표키워드')
    photo = models.ImageField(blank=True, verbose_name='대표사진', upload_to="blog/%Y/%m/%d")
    photo_description = models.TextField(max_length=50, blank=True, verbose_name='대표사진설명')
    #is_publish_ok = models.CharField(max_length=1, choices=PUBLISH_STATUS_CHOICES, default='d', verbose_name='글공개')
    is_publish_ok = models.BooleanField(choices=PUBLISH_STATUS_CHOICES, default=False, verbose_name='글공개')
    tags = TaggableManager()
    hits = models.IntegerField(default=0, verbose_name='조회수')
    created_at = models.DateField(auto_now_add=False, default=timezone.now, verbose_name='발행일')
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
