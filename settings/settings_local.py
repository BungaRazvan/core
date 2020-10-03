SECRET_KEY = 'inr)f_*ojrc-^&5m_x_3np*h4i!4m8!*!761pb%5@xqx)6a3fp'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'PASSWORD': '',
        'NAME': 'cms',
        'USER': 'root'
    }
}