"""
封装 Django ORM，方便脚本使用
"""
from django.conf import settings
import django
from easy_queryset import db_router

settings.configure(DEBUG=True)
settings.DATABASE_ROUTERS = ['easy_queryset.db_router.DatabaseAppsRouter']
django.setup()


def wrap_db(func):
    def inner(*args, **kwargs):
        app_label = kwargs.get('app_label', 'default')
        db_router.DATABASE_MAPPING[app_label] = app_label
        return func(*args, **kwargs)
    return inner


@wrap_db
def add_mysql(host, user, password, db, port=3306, app_label="default"):
    settings.DATABASES[app_label] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }


@wrap_db
def add_postgresql(host, user, password, db, port=3306, app_label="default"):
    settings.DATABASES[app_label] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }


@wrap_db
def add_sqlite(name, app_label="default"):
    settings.DATABASES[app_label] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': name,
    }


@wrap_db
def add_oracle(host, user, password, db, port=1521, app_label="default"):
    settings.DATABASES[app_label] = {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': db,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
