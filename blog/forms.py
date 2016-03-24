from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=70)
    name = forms.CharField(max_length=35, required=True)
    sender = forms.EmailField(max_length=35, required=True)
    message = forms.CharField(widget=forms.Textarea(), required=True)
    cc_myself = forms.BooleanField(required=False)


# class CountryCheckList(forms.Form):
#     REGION = ('MAJOR', 'MENA', 'LA', 'SEA', 'EUR',)
#
#     country = forms.CharField(max_length=75)
#     region = models.CharField(max_length=25, choices=ACTOR)