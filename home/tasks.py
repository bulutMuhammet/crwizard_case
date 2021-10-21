import json
from pyexpat import ExpatError

import dictdiffer
import xmltodict
from django.contrib.auth.models import User
from django.core.mail import send_mail
from json2xml import json2xml
from json2xml.utils import readfromstring

from crwizard_case.celery import app
from home.models import UploadedXML


@app.task(name="upload_and_parse")
def upload_and_parse(file_id,user):
    file = UploadedXML.objects.get(id=file_id)
    user = User.objects.get(username=user)
    xml_file = file.temp_xml
    try:
        parsed = xmltodict.parse(xml_file)
        parsed_dictionary = dict(parsed)

        file.xml_file = xml_file
        file.json_content = parsed_dictionary
        file.save()
        message = "XML dosyanız başarıyla sistemimize yüklenip veritabanına kaydedildi."

    except ExpatError:
        message = "XML dosyanız geçerli formatta değil, ya da yüklediğiniz dosya bir XML dosyası değil."
        file.delete()
    send_mail(subject="XML Yüklemesi", message=message,
              from_email='testmest5398@gmail.com',
              recipient_list=[user.email], fail_silently=False)

@app.task(name="change_content")
def change_content(file_id,json_content):
    file = UploadedXML.objects.get(id=file_id)

    if dict(file.json_content) == dict(json_content):
        message = "Yolladığınız xml önceki ile aynı olduğu için bir değişiklik yapılmadı"
    else:
        differences = []
        for diff in list(dictdiffer.diff(dict(file.json_content), dict(json_content))):
            differences.append(diff)
        file.json_content = json_content
        data = readfromstring(
            json.dumps(file.json_content)
        )
        xml_file = json2xml.Json2xml(data).to_xml()
        with open(file.xml_file.path, 'w') as fi:
            fi.write(xml_file)
            fi.close()
        file.save()
        message = """Değişiklik başarıyla yapıldı. İşte değişiklikler:\n"""
        try:
            for diff in differences:
                message += f"{diff[1]} konumundaki değişiklik: ({diff[2][0]}) -> ({diff[2][1]}) \n"
        except:
            message += "Rapor hazırlanırken bir sorun olşutu"


    send_mail(subject="XML Değişikliği", message=message,
              from_email='testmest5398@gmail.com',
              recipient_list=[file.user.email], fail_silently=False)