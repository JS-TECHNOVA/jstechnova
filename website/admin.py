from django.contrib import admin
from . import models
from django.conf import settings
import csv
from django.shortcuts import HttpResponse
# Register your models here.

admin.site.register(models.Services)
admin.site.register(models.Testimonial)
admin.site.register(models.UserQueries)

admin.site.register(models.TelegramClients)
admin.site.register(models.Projects)
admin.site.register(models.UserFeedbacks)


@admin.action(description="Export")
def exportEventRegistration(modeladmin, req, queryset):

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="rgistrations-data.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Phone", "College name", "Occupation", "Address"])
    writer.writerows(
        [
            [x.name, x.email, x.phone, x.college_name, x.occupation, x.addres] for x in queryset
        ]
    )

    return response

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ("registered_at", )
    ordering = ("name",)
    list_display = ("name", "email","phone", "occupation", "college_name")
    actions = (exportEventRegistration, )
    list_filter = ["event"]

admin.site.register(models.EventRegistrations, EventAdmin)



class EventsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title", "speaker")
    }
admin.site.register(models.Events, EventsAdmin)
admin.site.register(models.Team)



@admin.action(description="Mark selected blogs as published")
def publishblog(modeladmin, request, queryset):
    queryset.update(status="published")




# from django import forms

# class WYSIWYGWidget(forms.Textarea):
#     class Media:
#         css = {
#             'all': ('https://cdn.jsdelivr.net/npm/quill@1.3.6/dist/quill.snow.css',)  # Add your editor's CSS
#         }
#         js = ('https://cdn.jsdelivr.net/npm/quill@1.3.6/dist/quill.min.js',)  # Add your editor's JS

#     def __init__(self, attrs=None):
#         default_attrs = {'class': 'wysiwyg-editor'}  # Add necessary classes
#         if attrs:
#             default_attrs.update(attrs)
#         super().__init__(default_attrs)




class BlogsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    actions = (publishblog, )
    
admin.site.register(models.Blogs, BlogsAdmin)
