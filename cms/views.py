from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
# Create  views here.
from website import models


class HomeView(View):
    def get(self, req):
        return render(req, "cms/home.html")



class BlogsView(View):
    def get(self, request):
       return render(request, "cms/postBlog.html")
    
    def post(self, request):
        data = request.POST

        models.Blogs.objects.create(
            title = data.get("title"),
            image = request.FILES.get("image"),
            content = data.get("blog-content"),
            author = request.user,
            status = data.get("status")
        )

        return redirect("post_blog")





class UserBlogs(View):
    def get(self, request):
        blogs = models.Blogs.objects.filter(author = request.user)
        
        return render(request, "cms/myBlogs.html", {"blogs": blogs})



class LoginView(View):
    template = "cms/login.html"
    def get(self, request):
        return render(request, self.template)
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        context = {
            "username":username,
        }

        if username and password:
            user = authenticate(username=username, password = password)
            if user is not None and (user.is_staff or user.is_superuser):
                login(request, user)
                return redirect("cms_home")
            else:
                context["error"] = "Invalid login details."
        else:
            context["error"] = "All fields are required."
        return render(request, self.template, context=context)


class DeleteBlog(View):
    def get(self, request, blog_id):
        blog = models.Blogs.objects.filter(slug = blog_id)
        if blog.exists():
            blog.delete()
        return redirect("user_blogs")