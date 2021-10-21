from django import forms
from django_json_widget.widgets import JSONEditorWidget
from .models import UploadedXML

class ContentForm(forms.ModelForm):
    class Meta:
        model = UploadedXML

        fields = ('json_content',)

        widgets = {
            'json_content': JSONEditorWidget
        }