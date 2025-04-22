from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from . import models
from django.views import View
from . import forms
from django.contrib import messages
from .utils import sendTelegramMessage
from markdown import markdown


class HomeView(View):
    template_name = "website/index.html"

    def get(self, request, *args, **kwargs):
        # messages.success(request, "asdfasd")
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context = {}
        context["services"] = self.get_services
        context["testimonials"] = self.get_tesimonials
        context["contact_form"] = forms.ContactUsForm()
        return context
    

    def post(self, request, *args, **kwargs):
        f = forms.ContactUsForm(data=request.POST)
        if f.is_valid():
            if f.save():
                messages.success(request, "Form saved successfully. We will contact you soon.", )
                sendTelegramMessage(
                    header="New Contact Form filled",
                    body=f"Service type: { [f.cleaned_data['service']]}", 
                    sender_email=f.cleaned_data["email"], 
                    sender_name=f.cleaned_data["name"], 
                    sender_phone=f.cleaned_data["phone"]
                )
                return redirect("homepage",permanent=True)
            else:
                messages.error(request, "Failed to save. Please try again")
            c = self.get_context_data()
            c['contact_form'] = f
            return render(request, self.template_name, context=c)
        else:
            messages.warning(request,f.errors)
            c = self.get_context_data()
            c['contact_form'] = f
            return render(request, self.template_name, context=c)

    @classmethod
    def get_services(self):
        return models.Services.objects.all()
    
    @classmethod
    def get_tesimonials(self):
        return models.Testimonial.get_n_latest(4)


class BlogView(View):
    template_name = "website/Blogs.html"

    def get(self, request, slug = None):
        context = {}
        if not slug:
            context["blogs"] = models.Blogs.objects.filter(status="published").order_by("-created_at")
            return render(request, self.template_name, context=context)
        
        blog = models.Blogs.objects.filter(slug__iexact=slug)
        if blog.exists():
            context["content"] = blog[0].content
            context["blog"] = blog[0]
        else:
            context["error"] = True

        return render(request, "website/DetailedBlog.html",  context=context)
    

    def markdown(self, content):
        return markdown(content)

class ProjectsView(View):
    template_name = "website/Projects.html"
    def get(self, request):
        p = models.Projects.objects.all().order_by("id")
        return render(request, self.template_name, context={"projects": p, "services":models.Services.objects.all()})
    

class FeedbackView(View):
    
    def get(self, req):
        return render(req, "website/feedback.html")
    
    def post(self, request, *args, **kwargs):
        name, message, rating, email  = request.POST.get('name'), request.POST.get('message'), request.POST.get('rating'), request.POST.get('email')
        if not (message or rating or name or email):
            err = "Please fill the form correctly."
            return render(request, 'feedback.html',{"error": err, "message": message, "email": email, "name": name})
        else:
            models.UserFeedbacks.objects.create(
                name = name,
                experience = rating,
                email = email,
                message = message
            )
            messages.success(request, f"Thank you {name} for your valuable feedback. It's truly appreciated and will help us improve!")
            sendTelegramMessage(header="A New Feedback",body=message,sender_name=name,sender_phone= rating, sender_email= email)
            return redirect('feedback')



class EventsView(View):
    def get(self, request, slug = None):
        context = {}

        current_events = models.Events.objects.filter(
            status = 'open'
        )
        
        past_events = models.Events.objects.filter(
            status = "closed"
        )

        context["past_events"] = past_events

        if current_events.exists():
            context["current_event"] = current_events[0]
        else:
            if past_events.exists():
                context["current_event"] = past_events[0]

        return render(request, "website/Events.html", context=context)

class EventsDetailedView(View):
    def get(self, request, slug):
        event = models.Events.objects.filter(slug = slug)
        if event.exists():

            timeline = []
            for x in event[0].timeline.split("||"):
                timeline.append(markdown(x))
            
            context = {
                "event": event[0],
                "timeline": timeline,
                "about": markdown( event[0].about_event ),
            }
            if event[0].status != 'closed':
                context["form"]= forms.EventRegistrationForm()

            return render(request, "website/event-detailed.html", context= context)
        else:
            return redirect("events")
    
    def post(self, request, slug):
        form = forms.EventRegistrationForm(request.POST)
        event = models.Events.objects.filter(slug = slug)
        
        if form.is_valid():
            form.save()
            messages.success(request, "You entry has been registered. Stay tuned for further updates!")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, form.errors)
            
            timeline = []
            for x in event[0].timeline.split("||"):
                timeline.append(markdown(x))

            context = {
                "form": form,   
                "event": event[0],
                "timeline": timeline,
                "about": markdown( event[0].about_event ),
            }
            
            return render(request, "website/event-detailed.html", context=context)


class CareersView(View):

    def get(self, request):
        return render(request, "website/Careers.html")


class TeamView(View):
    def get(self, request):
        teams = models.Team.objects.all()
        return render(request, "website/TeamPage.html", {"teams":teams})

def TnC(req):
    return render(req, "website/TnC.html")
def PrivayPolicy(req):
    return render(req, "website/PP.html")