import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UploadedXML(models.Model):
    user = models.ForeignKey(User,related_name="files",on_delete=models.CASCADE)
    json_content = models.JSONField(default="{}")
    xml_file = models.FileField(upload_to="files/")
    temp_xml = models.FileField(upload_to="temp_files/")
    created_date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.xml_file.name)