from django.shortcuts import render
from blog.models import Category, Post, SiteInfo
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def post_index(request):
    print('여기까지 왔따')
    qs = Category.objects.filter(is_publish_ok=True).prefetch_related(Prefetch('post_set', queryset=Post.objects.filter(is_publish_ok=True)))
    print('여기는 어떨까?')
    print('qs', qs)
    return render(request, 'blog/post_index.html',{
        'categorys' : qs,
    })


def post_list(request):
    pass


def search_post_list(request):
    pass

def post_detail(request):
    pass

def tag_post_list(request):
    pass


def auto_write(request):
    pass