from django.urls import path
from . import views
urlpatterns = [
    path("login", views.LoginView.as_view(), name="cms_login"),
    path("", views.HomeView.as_view(), name="cms_home"),
    path("post-blog", views.BlogsView.as_view(), name="post_blogs"),
    path("blogs/myblogs", views.UserBlogs.as_view(), name="user_blogs"),
    path("blogs/myblogs/delete/<slug:blog_id>", views.DeleteBlog.as_view(), name=""),
]