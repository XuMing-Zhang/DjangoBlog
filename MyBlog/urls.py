"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_blogs),
    path('contact/', views.contact),
    path('post/', views.post),
    path('list/', views.my_blog_list),
    path('login/', views.login),
    path('logout/', views.logout),
    re_path(r'^detail/(\d+)/$', views.get_details, name='blog_get_detail'),
    re_path(r'^contact_del/(\d+)/$', views.contact_del),
    re_path(r'^blog_del/(\d+)/$', views.blog_del),
    re_path(r'^blog_edit/(\d+)/$', views.blog_edit),
    re_path(r'catagory/(\d+)/$', views.catagory),
    re_path(r'^archives/(\d+)/(\d+)/$', views.archives),
    #第三方模块URLconf
    re_path(r'^captcha/', include('captcha.urls')),#captcha验证码模块
    re_path(r'^accounts/', include('django_registration.backends.one_step.urls')),#Django-registration用户注册模块
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
]