from django.urls import path
from . import views
from .sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib import sitemaps
from .import models

info_dict = {
    "queryset": models.Blogs.objects.filter(status="published"),
    "date_field": "created_at",
}


all_sitemaps = {
    "static": StaticViewSitemap,
    "blogs": sitemaps.GenericSitemap(info_dict=info_dict, priority=0.6, changefreq="monthly")
}


urlpatterns = [
    path("", views.HomeView.as_view(), name="homepage"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("blogs/", views.BlogView.as_view(), name="blogs"),
    path("blogs/<slug:slug>/", views.BlogView.as_view(), name=""),
    path("terms-and-conditions/", views.TnC, name="terms-and-conditions"),
    path("privacy-policy/", views.PrivayPolicy, name="privacy-policy"),
    path("feedback/", views.FeedbackView.as_view(), name="feedback"),
    path("careers/", views.CareersView.as_view(), name="careers"),
    path("team/", views.TeamView.as_view(), name="team"),
    path("events/", views.EventsView.as_view(), name="events"),
    path("events/<slug:slug>/", views.EventsView.as_view(), name=""),

    path("sitemap.xml/",sitemap,{"sitemaps": all_sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]
