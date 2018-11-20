from django.contrib import admin


from blog.models import *
admin.site.register([Catagory, Tag, Blog, Contact, UserInfo])
