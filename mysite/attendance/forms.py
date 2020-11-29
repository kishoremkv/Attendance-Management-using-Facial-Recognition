from django import forms
from django.forms import ClearableFileInput
from .models import UploadFile  
class FileUpload(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['files']
        widgets = {
            'files': ClearableFileInput(attrs={'multiple'
            : True}),
        }