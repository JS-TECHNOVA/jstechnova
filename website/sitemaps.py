from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "never"

    def items(self):
        return ["homepage","projects", "blogs", "terms-and-conditions", "privacy-policy", "feedback", "careers", "team", "events"]

    def location(self, item):
        return reverse(item)
    