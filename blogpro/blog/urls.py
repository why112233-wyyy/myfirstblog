# -*- coding:utf-8 -*-
"""
模块描述：

作者：why
"""
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('mypost/', views.my_post_list, name='my_post_list'),
    path('creablog/', views.create_blog, name='creablog'),
    path(
        '<int:year>/<int:month>/<int:day>/<str:slug>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        '<str:slug>/delete/',
        views.PostDeleteView.as_view(),
        name='post_delete'
    ),
    path(
        '<str:slug>/update/',
        views.blog_update,
        name='blog_update'
    ),
    path('tag/<str:tag_slug>/',
         views.post_list, name='post_list_by_tag'),

]
