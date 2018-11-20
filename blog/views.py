from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from blog.models import *
from blog.forms import CommentForm, ContactForm, BlogModelForm, LoginForm

from markdown import markdown


def get_blogs(request):
    """
    获取所有用户博客条目并分页显示，且只显示管理员审核后的内容，由数据库中enable字段控制。
    """
    if request.user.is_authenticated:
        # Django auth用户验证系统，如果用户是验证通过的就返回True;
        username = request.user.username
        # 将当前登陆的用户名赋值给username;
    blogs = Blog.objects.filter(enable=True).order_by('-created')
    # enable=True的查询结果集，并以发布时间降序排列；

    paginator = Paginator(blogs, 6, 2)
    # 实例化结果集，每页6条数据，少于2条合并到上一页；

    page = request.GET.get('page', 1)
    # 接收网页中的page；

    try:
        blog_pages = paginator.page(page)
        # 获取当前页面的结果集；
    except PageNotAnInteger:
        # 如果用户在url栏后的?page=输入的不是一个整数，将显示第一页的内容；
        blog_pages = paginator.page(1)
    except EmptyPage:
        # 如果输入的页数大于当前页码，将显示最后一页内容；
        blog_pages = paginator.page(paginator.num_pages)

    # context = {'blog_pages': blog_pages, 'username': username} # 构造上下文；

    return render(request, 'blog_list.html', locals())
    # local()函数可以将函数体内所有的变量打包传递到前端'blog_list.html'中；


def get_details(request, blog_id):
    """
    根据选择博客文章的id，显示该博客文章的详细内容，并加入评论功能，评论功能采用Form表单实现；
    """
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    try:
        blog = Blog.objects.get(id=blog_id)
        blog.content = markdown(blog.content)
        # 获取用户所选文章id的一个查询结果；
    except Blog.DoesNotExist:
        # 如果用户在url栏输入了一个不存在的文章id，将返回Http404页面；
        raise Http404
    if request.method == 'GET':
        # 如果页面请求方式为GET
        form = CommentForm()
        # 依据forms向前端传递一个空表单；
    else:

        form = CommentForm(request.POST)

        # 如果页面请求方式为POST（点击了提交按钮），则将用户在表单中输入的内容对象赋值给form变量；
        if form.is_valid():
            # 检查窗体各个字段输入的内容是否正确；
            cleaned_data = form.cleaned_data
            # 将form中的数据保存至变量,字典类型
            cleaned_data['blog'] = blog
            # 和博文建立关联，这样就可以查询到这个评论是针对那篇博文的评论了；
            Comment.objects.create(**cleaned_data)
            # 将数据保存到数据库中，cleaned_data为字典类型，前面加两个*就可以直接保存到数据库中；
        return redirect('.')
        # 以GET的请求方式刷新当前页；
    context = {
        'username': username,
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-created'),
        # 反向查询，通过主表查询子表数据，每个主表的对象都有一个是外键的属性，可以通过它来查询到所有属于主表的子表的信息
        # 这个属性的名称默认是以子表的名称小写加上_set()来表示，默认返回的是一个querydict对象
        'form': form
    }
    return render(request, 'blog_details.html', context)


def contact(request):
    """
    联系管理员功能；
    """
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Contact.objects.create(**cleaned_data)
            messages.add_message(request, messages.SUCCESS, '您的意见或建议已经成功发送给管理员！')
            return redirect('/contact')
    return render(request, 'contact.html', locals())


def contact_del(request, nid):
    """
    删除“发给管理员的内部消息”
    """
    Contact.objects.filter(id=nid).delete()
    # 根据前端所选的Contact.id，将信息删除；
    return redirect('/list/')


def post(request):
    """
    发布文章功能
    """
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    if request.method == 'GET':
        form = BlogModelForm()
    else:
        author_user = User.objects.get(username=username)
        # 在Django auth_user用户表中找到当前登陆的用户存放到变量中；
        post_auth = Blog(author_user=author_user)
        # 使用author_user执行实例去Blod的model中创建一个执行实例存放到变量中；
        form = BlogModelForm(request.POST, instance=post_auth)
        # 再把post_auth传递到用户提交的ModelForm表单中执行合并操作，最后得到的form是带有当前用户信息的博客文章；
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '您的文章发布成功,等待管理员审核后显示！')
            return redirect('/post/')
    return render(request, 'post.html', locals())


def login(request):
    """
    用户登陆及验证模块；使用Django内置的 auth用户验证功能。
    """
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            # 把从表单中取到的用户输入的用户名及密码通过authenticate函数在auth_user表中进行验证，如果用户存在且密码正确
            # 函数就会返回该用户的数据并存放在user变量中，否则返回None；
            if user is not None:
                # 检查用户是否验证通过；
                if user.is_active:
                    # 检查此账号的是否被激活；
                    auth.login(request, user)
                    # 将用户数据存入session中；
                    messages.add_message(request, messages.SUCCESS, '登陆成功！')
                    # 使用了Django的信息显示框架messages framework;除了SUCCESS状态外还包括DEBUG,INFO,WARNING,ERROR
                    # 也可以使用如下简写方法：messages.SUCCESS(request,'字符串')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.ERROR, '账号未激活，请联系管理员！')
            else:
                messages.add_message(request, messages.WARNING, '用户名或密码错误，请检查后再登陆！')
        else:
            messages.add_message(request, messages.WARNING, '请检查输入的字段内容')
    else:
        login_form = LoginForm()

    return render(request, 'login.html', {'login_form': login_form})


def logout(request):
    """
    用户退出功能，清空session;
    """
    request.session.clear()
    messages.add_message(request, messages.WARNING, '退出成功！')
    return redirect('/')


@login_required(login_url='/login/')
# 是auth验证机制提供的一个装饰器,以下函数是需要用户登陆后才执行的，如果没登陆将跳转到/login/页面，也就是登陆页面；
def my_blog_list(request):
    """
    用户登陆成功和，可以查看自己所发布的博文；
    """
    if request.user.is_authenticated:
        username = request.user.username
        try:
            user = User.objects.get(username=username)
            # 在auth_user表中找到当前登陆的用户；
            blog_list = Blog.objects.filter(author_user=user, enable=True).order_by('-created')
            # 在Blog表中找到当前登陆用户发表的博文，且经过管理员审核后的；
            contact_list = Contact.objects.all().order_by('-created')
            # 取出所有用户联系管理员的信息；
            # 管理员为特定用户，我的方法是在前端通过模板语言判断是否为管理员登陆，如果是就显示所有发给管理员的信息，如果
            # 是普通用户，就不显示。
        except:
            pass

    return render(request, 'my_blog_list.html', locals())


def blog_del(request, nid):
    """
    删除自己发表的博文，但是并非物理删除，而是将enable字段重新修改为False，误删除可以联系管理员恢复。
    """
    Blog.objects.filter(id=nid).update(enable='False')
    return redirect('/list/')


def blog_edit(request, nid):
    """
    修改博客文章
    """
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    if request.method == 'GET':
        blog_obj = Blog.objects.filter(id=nid).first()
        # 找到对应文章id编号的的一个实例对象，如果不存在返回None
        mf = BlogModelForm(instance=blog_obj)
        # 用上面找到的实例对象为参数传递给ModelForm，这样在前端mf.as_p中将显示用户所选择的文章信息，以便修改。
        context = {'mf': mf, 'nid': nid, "username": username}
        return render(request, 'blog_edit.html', context)
    else:
        blog_obj = Blog.objects.filter(id=nid).first()
        # 找到对应文章id编号的的一个对象，如果不存在返回None
        mf = BlogModelForm(request.POST, instance=blog_obj)
        #
        if mf.is_valid():
            mf.save()
            messages.add_message(request, messages.SUCCESS, '文章修改成功！')
            return redirect('.')

        return render(request, 'blog_edit.html', locals())


def sidebar(request):
    catagorys = Catagory.objects.all()  # 从数据库中取出所有分类；

    return render(request, 'base.html', {'catagorys': catagorys})


def catagory(request, cid):
    """
    根据文章分类显示博文；
    """
    if request.user.is_authenticated:
        username = request.user.username

    catagory_list = Blog.objects.filter(catagory_id=cid).order_by('-created')
    # 从数据库取出所有从前端返回的文章分类id相等的博客文章对象；

    paginator = Paginator(catagory_list, 5, 2)
    # 实例化结果集，每页6条数据，少于6条合并到上一页；

    page = request.GET.get('page', 1)
    # 接收网页中的page；

    try:
        blog_pages = paginator.page(page)
        # 获取当前页面的结果集；
    except PageNotAnInteger:
        # 如果用户在url栏后的?page=输入的不是一个整数，将显示第一页的内容；
        blog_pages = paginator.page(1)
    except EmptyPage:
        # 如果输入的页数大于当前页码，将显示最后一页内容；
        blog_pages = paginator.page(paginator.num_pages)

    # context = {'blog_pages': blog_pages, 'username': username}  # 构造上下文；

    return render(request, 'catagory_blog_list.html', locals())


def archives(request, cyear, cmonth):
    """
    根据归档时间显示博文
    """
    if request.user.is_authenticated:
        username = request.user.username

    archive = Blog.objects.filter(author_user__blog__created__year=cyear,
                                  author_user__blog__created__month=cmonth).order_by('-created').distinct()
    paginator = Paginator(archive, 6, 2)
    # 实例化结果集，每页6条数据，少于2条合并到上一页；

    page = request.GET.get('page', 1)
    # 接收网页中的page；

    try:
        blog_pages = paginator.page(page)
        # 获取当前页面的结果集；
    except PageNotAnInteger:
        # 如果用户在url栏后的?page=输入的不是一个整数，将显示第一页的内容；
        blog_pages = paginator.page(1)
    except EmptyPage:
        # 如果输入的页数大于当前页码，将显示最后一页内容；
        blog_pages = paginator.page(paginator.num_pages)

    # context = {'blog_pages': blog_pages, 'username': username}  # 构造上下文；

    return render(request, 'archives_blog_list.html', locals())
