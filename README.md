# crwizard_case app

## Proje içinde sanal çevre oluşturulmalıdır

`pip install virtualenv
`
<br> <br>
`virtualenv venv 
`


### Sanal çevreyi deaktif etme:

`deactivate
`

### Sanal çevreyi aktif etme:

`
.\venv\Scripts\activate
`
# Gereklilikleri yükleme:

`pip install -r requirements.txt
`
# Migrations işlemleri:

`python manage.py makemigrations
` <br><br>
`python manage.py migrate
`


# Run:

`python manage.py runserver
`
# Superuser oluşturma

`python manage.py createsuperuser`


<hr>







# Üyelik

Gerekli google authentication api anahtarları admin panelinden tanımlanmalıdır.

Kontrol edin:
https://console.cloud.google.com/apis/

# Asenkron arka plan işlemleri
XML ayrıştırma ve düzenleme işlemlerinin uzun yükünü celery halletmektedir.

### Redis'i yükleme:

https://redis.io/download

Ardından redis-server çalıştırın


### Celery işçilerini çalıştırmak 

`celery -A crwizard_case.celery worker --loglevel=info -P eventlet`


### Mail

Mail işlemleri için basit bir gmail hesabı kullandım. İstenilirse settings.py üzerinden yeniden konfigüre edilebilir.



