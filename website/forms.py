from django import forms
from . import models


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=10, required=True)
    email = forms.EmailField(required=True)
    service = forms.ModelChoiceField(queryset= models.Services.objects.all(), required=True, empty_label="Select Service Type")
    message = forms.CharField(widget=forms.Textarea(), required=True)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if len(phone) != 10 or phone[0] in ["0",'1','2','3','4','5'] or not phone.isdigit():
            raise forms.ValidationError("Invalid phone number.")
        return phone

    
    def save(self):
        data = self.cleaned_data
        data["service_type"] = data["service"]
        del data["service"]
        
        try:
            models.UserQueries.objects.create(
                **data
            )
        except Exception as e:
            print(e)
            return False
        return True


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.EventRegistrations
        fields = "__all__"

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if len(phone) != 10 or phone[0] in ["0",'1','2','3','4','5'] or not phone.isdigit():
            raise forms.ValidationError("Invalid phone number.")
        return phone
