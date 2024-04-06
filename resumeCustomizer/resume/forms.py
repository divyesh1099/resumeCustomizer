from django import forms

class JobDescriptionForm(forms.Form):
    job_description = forms.CharField(widget=forms.Textarea)

class FileUploadForm(forms.Form):
    file = forms.FileField()

class CompanyNameForm(forms.Form):
    company_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter company name'}))

class RoleForm(forms.Form):
    role = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter role (e.g., SDE, MLE)'}))