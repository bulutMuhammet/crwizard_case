from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "home"

urlpatterns = [
    path('', views.index, name="index"),
    path('xml_files/delete/<int:file>', views.delete_xml, name="delete_xml"),
    path('xml_files/edit/<int:file>', views.edit_xml, name="edit_xml"),
    path('login', views.login, name="login"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
