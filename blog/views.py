from django.shortcuts import render
from blog.models import Category, Post, SiteInfo
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def post_index(request):
    qs = Category.objects.filter(is_publish_ok=True).prefetch_related(Prefetch('post_set', queryset=Post.objects.filter(is_publish_ok=True)))
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    return render(request, 'blog/post_index.html',{
        'categorys' : qs,
        'hit_posts' : hit_posts,
    })


def post_list(request):
    pass


def search_post_list(request):

    q = request.GET.get('q', '')
    categorys = Category.objects.filter(is_publish_ok=True)
    post = Post.objects.filter(title__icontains=q, is_publish_ok=True)
    paginator = Paginator(post, 6)
    page = request.GET.get('page')
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/search_post_list.html',{
        'q' : q,
        'categorys' : categorys,
        'posts' : posts,
        'page' : page,
        'hit_posts' : hit_posts,
    })

def post_detail(request, pk, slug):
    categorys = get_list_or_404(Category.objects.filter(is_publish_ok=True))
    post = get_object_or_404(Post, id=pk, slug=slug)
    Post.objects.filter(id=pk, slug=slug).update(hits = post.hits + 1)
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    related_qs = Post.objects.filter(category=post.category, is_publish_ok=True).exclude(id=pk)[:3]
    return render(request, 'blog/post_detail.html',{
        'post': post,
        'related_posts': related_qs,
        'categorys' : categorys,
        'hit_posts' : hit_posts,

    })

def tag_post_list(request, tag):

    categorys = Category.objects.filter(is_publish_ok=True)
    post = Post.objects.filter(tags__name__in=[tag], is_publish_ok=True)
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    paginator = Paginator(post, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/tag_post_list.html',{
        'tag' : tag,
        'categorys' : categorys,
        'posts' : posts,
        'page' : page,
        'hit_posts' : hit_posts,
    })


def auto_write(request):
    pass
