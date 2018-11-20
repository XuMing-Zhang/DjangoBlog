from django import template
from ..models import Blog, Catagory, Comment

register = template.Library()  # 实例化template.Library类；


@register.simple_tag  # 将函数recent_post_blog装饰为register.simple_tag;
def recent_post_blog(num=5):
    """
    获取数据库中最新发布的5条文章；
    """
    return Blog.objects.filter(enable=True).order_by('-created')[:num]


@register.simple_tag
def get_categories():
    """
    获取所有文章的分类
    """
    return Catagory.objects.all()


@register.simple_tag
def recent_comment(num=5):
    """
    获取数据库中最新5条评论；
    """
    return Comment.objects.all().order_by('-created')[:num]


@register.simple_tag
def archives():
    """
    文章归档：返回
    """
    return Blog.objects.dates('created', 'month', order='DESC')
