from django.shortcuts import render
from blog.models import Category, Post, SiteInfo
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext




def post_index(request):
    qs = Category.objects.filter(is_publish_ok=True).prefetch_related(Prefetch('post_set', queryset=Post.objects.filter(is_publish_ok=True)))
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    site_info = SiteInfo.objects.all()[:1]

    return render(request, 'blog/post_index.html',{
        'categorys' : qs,
        'hit_posts' : hit_posts,
        'site_info' : site_info,
    })


def post_list(request, category):

    q = request.GET.get('q', '')
    categorys = Category.objects.filter(is_publish_ok=True)

    if q:
        return search_post_list(request, q)
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    post = Category.objects.filter(category_name=category).prefetch_related('post_set')
    paginator = Paginator(post[0].post_set.filter(is_publish_ok=True), 6)
    site_info = SiteInfo.objects.all()[:1]

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
            posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {
        'category': posts,
        'page': page,
        'categorys' : categorys,
        'now_category' : category,
        'q' : q,
        'hit_posts' : hit_posts,
        'site_info' : site_info,
    })


def search_post_list(request):

    q = request.GET.get('q', '')
    categorys = Category.objects.filter(is_publish_ok=True)
    post = Post.objects.filter(title__icontains=q, is_publish_ok=True)
    paginator = Paginator(post, 6)
    page = request.GET.get('page')
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    site_info = SiteInfo.objects.all()[:1]
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
        'site_info' : site_info,
    })

def post_detail(request, pk, slug):
    categorys = Category.objects.filter(is_publish_ok=True)
    post = get_object_or_404(Post, id=pk, slug=slug, is_publish_ok=True)
    Post.objects.filter(id=pk, slug=slug).update(hits = post.hits + 1)
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    related_qs = Post.objects.filter(category=post.category, is_publish_ok=True).exclude(id=pk)[:3]
    site_info = SiteInfo.objects.all()[:1]

    return render(request, 'blog/post_detail.html',{
        'post': post,
        'related_posts': related_qs,
        'categorys' : categorys,
        'hit_posts' : hit_posts,
        'site_info' : site_info,

    })

def tag_post_list(request, tag):

    categorys = Category.objects.filter(is_publish_ok=True)
    post = Post.objects.filter(tags__name__in=[tag], is_publish_ok=True)
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    paginator = Paginator(post, 6)
    page = request.GET.get('page')
    site_info = SiteInfo.objects.all()[:1]

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
        'site_info' : site_info,
    })

@login_required
def auto_write(request):
    categorys = Category.objects.all()
    category_id = request.GET.get('category_id', '')
    blog_address = request.GET.get('blog_address', '')


    if blog_address:
        return blog_crawling(request, category_id, blog_address)

    return render(request, 'blog/auto_write.html',{
        'categorys': categorys,

    })

def blog_crawling(request, category_id, blog_address):
    import requests
    from bs4 import BeautifulSoup
    from datetime import date

    parse_url = blog_address
    categorys = Category.objects.all()

    if 'm.blog' in parse_url:
        html = requests.get(parse_url).text
        soup = BeautifulSoup(html, 'html.parser')
        new_parse_content = soup.select('div.se-main-container')
        old_parse_content = soup.select('div.se_component_wrap')
        more_old_parse_content = soup.select('div.post_ct')

        # new 스타일
        if len(new_parse_content) > 0:
            parse_title = soup.select('div.se-title-text')[0].text.strip()
            new_slug = parse_title.replace("/", "").replace("~", "").replace("?", "").replace(" ", "-").replace("[", "-").replace("]", "").replace("(", "-").replace(")", "").replace(",","-")
            parse_content = str(new_parse_content[0])

            # 블로그의 작성일을 가지고 와서 date객체를 생성한다.
            created_at_str = soup.find_all("p", "blog_date")[0].text.strip()
            created_at_str_list = created_at_str.split('.')
            created_at_year = created_at_str_list[0]
            created_at_month = created_at_str_list[1]
            created_at_day = created_at_str_list[2]
            created_at_time = date(int(created_at_year), int(created_at_month), int(created_at_day))


        # naver blog old style
        elif len(old_parse_content) > 0:
            parse_title = soup.select('div.se_title')[0].text.strip()
            new_slug = parse_title.replace("/", "").replace("~", "").replace("?", "").replace(" ", "-").replace("[", "-").replace("]", "").replace("(", "-").replace(")", "").replace(",","-")
            parse_content = str(old_parse_content[1])

            # 블로그의 작성일을 가지고 와서 date객체를 생성한다.
            created_at_str = soup.find_all("p", "blog_date")[0].text.strip()
            created_at_str_list = created_at_str.split('.')
            created_at_year = created_at_str_list[0]
            created_at_month = created_at_str_list[1]
            created_at_day = created_at_str_list[2]
            created_at_time = date(int(created_at_year), int(created_at_month), int(created_at_day))

        # naver blog more old style
        elif len(more_old_parse_content) > 0:
            parse_title = soup.select('div.tit_area')[0].text.strip()
            new_slug = parse_title.replace("/", "").replace("~", "").replace("?", "").replace(" ", "-").replace("[", "-").replace("]", "").replace("(", "-").replace(")", "").replace(",","-")
            parse_content = str(more_old_parse_content[0])

            # 블로그의 작성일을 가지고 와서 date객체를 생성한다.
            created_at_str = soup.find_all("p", "se_date")[0].text.strip()
            created_at_str_list = created_at_str.split('.')
            created_at_year = created_at_str_list[0]
            created_at_month = created_at_str_list[1]
            created_at_day = created_at_str_list[2]
            created_at_time = date(int(created_at_year), int(created_at_month), int(created_at_day))

        else:
            messages.info(request, '크롤링 URL 정확하게 입력해주세요.')
            return render(request, 'blog/auto_write.html', {
                'categorys': categorys
            })

        #카테고리를 가지고 온다.
        new_cat = Category()
        new_cat.id = int(category_id)


        #포스트를 생성한다.
        new_post = Post.objects.create(category=new_cat, title=parse_title, slug=new_slug, content=parse_content, is_publish_ok=False, created_at=created_at_time)

        #블로그에서 사용된 태그를 가지고 온다.(new style, old style, more old style 모두 태그가 동일하다.
        tags = soup.select('div.post_tag > ul > li > a > span')


        tag_list = []
        #태그가 한번도 사용된 적이 없으면 새로 생성하고 new_post에 태그를 추가한다.
        for tag in tags:
            tag = tag.text.replace('#', '')
            new_post.tags.add(tag)
            # tag_list.append(tag)
            # tag_qs = Tag.objects.filter(name=tag)

            #태그가 생성된 적이 없으면 태그를 생성하고 new_post에 추가한다.
            # if tag_qs.exists() is False:
            #     post_tag = Tag.objects.create(name=tag)
            #     new_post.tag_set.add(post_tag.id)
            # #태그가 생성된적이 있으면 그냥 new_post에 추가한다.
            # else:
            #     post_tag = Tag.objects.get(name=tag)
            #     new_post.tag_set.add(post_tag.id)



        if new_post:
            messages.info(request, '크롤링하여 저장에 성공했습니다.')
        else:
            messages.info(request, '포스팅 저장에 실패했습니다.')

    else:
        messages.info(request, '모바일주소를 정확하게 입력해주세요')

    return render(request, 'blog/auto_write.html', {
        'categorys' : categorys
    })

def page_not_found_page(request, exception):
    
    categorys = Category.objects.filter(is_publish_ok=True)
    hit_posts = Post.objects.filter(is_publish_ok=True).order_by('-hits')[:5]
    post = Category.objects.all()
    paginator = Paginator(post[0].post_set.filter(is_publish_ok=True), 6)
    page = request.GET.get('page')
    site_info = SiteInfo.objects.all()[:1]

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
            posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/404.html', {
        'category': posts,
        'page': page,
        'categorys' : categorys,
        'hit_posts' : hit_posts,
        'site_info' :site_info,
    }) 


