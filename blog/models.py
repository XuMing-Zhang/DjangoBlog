from django.db import models
from django.contrib.auth.models import User


class Catagory(models.Model):
    """
    博客文章分类Model
    """
    name = models.CharField('名称', max_length=30)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客文章标签Model
    """
    name = models.CharField('名称', max_length=16)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    博客正文Model
    """
    title = models.CharField('标题', max_length=32)
    content = models.TextField('博客正文')
    created = models.DateTimeField('发布时间', auto_now_add=True)
    enable = models.BooleanField(default=False, null=True)  # 只有当管理员在admin页面手动取消勾选后，发布的信息才能显示，起到审核作用。
    catagory = models.ForeignKey(to=Catagory, verbose_name='分类', on_delete=models.CASCADE)
    author_user = models.ForeignKey(to=User, verbose_name='作者', on_delete=models.CASCADE)
    tags = models.ManyToManyField(to=Tag, verbose_name='标签')

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    博客文章评论Model
    """
    blog = models.ForeignKey(to=Blog, verbose_name='博客', on_delete=models.CASCADE)
    name = models.CharField('称呼', max_length=16)
    email = models.EmailField('邮箱')
    content = models.CharField('内容', max_length=240)
    created = models.DateTimeField('发布时间', auto_now_add=True)

    def __str__(self):
        return self.content


class Contact(models.Model):
    """
    联系管理员Model
    """
    name = models.CharField('称呼', max_length=16)
    email = models.EmailField('邮箱')
    content = models.CharField('内容', max_length=240)
    captcha = models.CharField('验证码', max_length=8)
    created = models.DateTimeField('发布时间', auto_now_add=True)

    def __str__(self):
        return self.content


class UserInfo(models.Model):
    """
    使用django提供的auth用户验证后，此model作废；
    """
    username = models.CharField('用户名', max_length=16)
    email = models.EmailField('邮箱')
    password = models.CharField('密码', max_length=16)
    enable = models.BooleanField(default=False)
    captcha = models.CharField('验证码', max_length=8)

    def __str__(self):
        return self.username
