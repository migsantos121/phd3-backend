# phd3 backend

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DAJNGO_SETTINGS_MODULE = "phd3_backend.settings.local"
python manage.py build -ad -b alpha
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Point your browser at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)


Refer below urls for api documentation:

* [https://s3.ap-south-1.amazonaws.com/phd3-backend-media-static/api-docs/alpha/index.html](https://s3.ap-south-1.amazonaws.com/phd3-backend-media-static/api-docs/alpha/index.html)
