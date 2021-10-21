from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import json

from home.forms import ContentForm
from home.models import UploadedXML
from home.tasks import upload_and_parse, change_content


@login_required(login_url="home:login")
def index(request):
    if request.method == "POST":

        ## yüklenen dosyayı kontrol için temp_xml alanına kaydet
        up = UploadedXML.objects.create(user=request.user, temp_xml=request.FILES.get("file"))
        upload_and_parse.delay(up.id,request.user.username)
        messages.success(request,"İstek kuyruğa alındı. İşlem gerçekleştiğinde eposta ile bilgilendirileceksiniz ")


    files = request.user.files.filter().exclude(json_content="{}")
    context = {"files":files}
    return render(request, "index.html",context)


def delete_xml(request,file):
    UploadedXML.objects.get(id=file).delete()
    messages.success(request,"Başarıyla silindi...")
    return redirect("home:index")

def edit_xml(request,file):
    file  = UploadedXML.objects.get(id=file)
    form = ContentForm(request.POST or None,instance=file)
    context = {"form":form}

    if request.method=="POST":
        json_content = json.loads(request.POST.get("json_content"))
        change_content.delay(file.id,json_content)
        messages.success(request,"İstek kuyruğa alındı. İşlem gerçekleştiğinde eposta ile bilgilendirileceksiniz ")

        return redirect("home:index")
    return render(request, "edit.html",context=context)

def login(request):
    return render(request,"login.html")


