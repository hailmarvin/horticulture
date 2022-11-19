from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs', views.blog, name='blogs'),
    path('blogs/<str:pk>', views.blog_profile, name='blog-profile'),
    path('news', views.news, name='news'),
    path('news/<str:pk>', views.news_profile, name='news-profile'),
    path('user/<str:user_id>/change/', views.change),
    path('auth', views.authentication, name='authentication'),
    path('upload-blog', views.upload_blog, name='upload-blog'),
    path('upload-news', views.upload_news, name='upload-news'),
    path('delete-user/<int:pk>', views.del_user, name='delete-user'),
    path('blogs/<str:pk>/update', views.update_blog, name='update-blog'),
    path('news/<str:pk>/update', views.update_news, name='update-news'),
    path('blogs/<str:pk>/delete', views.delete_blog, name='delete-blog'),
    path('news/<str:pk>/delete', views.delete_news, name='delete-news'),
    path('logout', views.signout, name='logout'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('search', views.search, name='search'),
    path('gallery', views.gallery, name='gallery'),
    path('upload-gallery', views.upload_gallery, name='upload-gallery')
]