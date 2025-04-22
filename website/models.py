from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Services(models.Model):
    image = models.ImageField(upload_to="uploads/services")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class Testimonial(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=40)
    message = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="uploads/testimonials")
    display = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name
    
    @staticmethod
    def get_n_latest(n):
        return Testimonial.objects.all().order_by("-created_at")[:5]
    

class UserQueries(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    service_type = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=1500)

    def __str__(self):
        return self.name + ' ' + self.phone


class TelegramClients(models.Model):
    name = models.CharField(max_length= 100)
    chat_id = models.CharField(max_length= 50)

    class Meta:
        verbose_name = 'telegram client'

    @staticmethod
    def all():
        return TelegramClients.objects.all()
    def __str__(self):
        return self.name
    


class Projects(models.Model):

    name = models.CharField(max_length=50)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=600)
    image = models.ImageField(upload_to="uploads/projects")

    def __str__(self):
        return self.name


class UserFeedbacks(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    experience = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.CharField(max_length=1500)

    def __str__(self):
        return self.name + ' ' + self.email



class Team(models.Model):
    name = models.CharField(max_length=30)
    designation = models.CharField(max_length=50)
    image = models.ImageField(upload_to="uploads/team/")
    linkedin = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.name




STATUS_CHOICES = ( 
('draft', 'Draft'), 
('published', 'Published'), 
) 

class Blogs(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="uploads/blogs")
    content = models.TextField()
    # author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    slug = models.SlugField(max_length = 250, null = True, blank = True) 
    updated = models.DateTimeField(auto_now = True) 

    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, 
                                                    default ='draft') 
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blogs/{self.slug}/"
    


EVENT_STATUS = [
    ("open", "Taking Registrations"),
    ("closed", "Not Taking Registrations"),
    ("upcoming", "Up Coming Event")
]

class Events(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, max_length = 1000)
    image = models.ImageField(upload_to="uploads/blogs")
    event_date =  models.DateField()
    # youtube_link
    yt_link = models.URLField(null=True, blank=True)

    about_event = models.TextField(max_length=15000)

    mode = models.TextField(max_length=50,choices=[("Online","Online"), ("Offline", ("Offline"))])

    timeline = models.TextField(max_length=10000, null=True, blank=True)

    seats = models.IntegerField(default=0)

    #speaker details
    speaker = models.CharField(max_length= 100)
    speaker_designation = models.CharField(max_length=100, default="")
    about_speaker = models.CharField(max_length=300)
    speaker_photo = models.ImageField(upload_to="uploads/speakers", null=True, blank=True)

    slug = models.SlugField(max_length = 250, null = True, blank = True)

    status = models.CharField(max_length = 10, choices = EVENT_STATUS, 
                                                    default ='upcoming') 
    def __str__(self):
        return self.title
    

class EventRegistrations(models.Model):

    registered_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    occupation = models.CharField(max_length=100)
    college_name = models.CharField(verbose_name="College name if you are a student", max_length=200)
    addres = models.CharField(max_length=300, verbose_name="Address")
    
    event = models.ForeignKey(Events, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.name