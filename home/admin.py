from django.contrib import admin
from .models import UploadedXML
from django_json_widget.widgets import JSONEditorWidget
from django.db import models


@admin.register(UploadedXML)
class UploadedXMLAdmin(admin.ModelAdmin):
    list_display = ["user","created_date"]
    exclude =('temp_xml',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    class Meta:
        model=UploadedXML