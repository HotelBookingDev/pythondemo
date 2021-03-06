from __future__ import absolute_import
"""
Django Alipaysettings for hotelBookingProject project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/Alipaysettings/

For the full list of Alipaysettings and their values, see
https://docs.djangoproject.com/en/1.9/ref/Alipaysettings/
"""

import os
import django
import manage
import datetime
from datetime import timedelta
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
BASE_DIR = os.path.dirname(os.path.realpath(manage.__file__))
STATICFILES_DIRS = (
)
STATIC_URL = '/static/'
# 以下的配置是自己加的
# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 文件夹 是用来将所有STATICFILES_DIRS中所有文件夹中的文件，以及各app中static中的文件都复制过来
# 把这些文件放到一起是为了用apache等部署的时候更方便
# 当调用collect staticfile时 放置的文件夹
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Quick-start development Alipaysettings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3p25-g&26g!kq%7bpqe1qxq^xa9hzgw)d)b_*7bf0iv8^kbiyt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# support celery
import djcelery
from celery.schedules import crontab
# BROKER_URL = 'redis://:Zhuo8995588@3e5069637587473d.redis.rds.aliyuncs.com:6379/DB0'
# todo 注意，我在 celery.py中覆盖了这些行为
BROKER_URL = 'django://'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'  #配置结果的存储
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False # 不是用UTC
CELERY_TASK_RESULT_EXPIRES = 10 #任务结果的时效时间
CELERY_SEND_TASK_ERROR_EMAILS = True
ADMINS = (
    ('George Costanza', 'nimdanoob@163.com'),
)

# Email address used as sender (From field).
SERVER_EMAIL = 'chaomengshidai@agesd.com'
# Mailserver configuration
# EMAIL_HOST_USER = 'servers'
# EMAIL_HOST_PASSWORD = 's3cr3t'
CELERYD_LOG_FILE = BASE_DIR + "/logs/celery/celery2.log" # log路径
CELERYBEAT_LOG_FILE = BASE_DIR + "/logs/celery/beat.log" # beat log路径
CELERYBEAT_SCHEDULE = {
    # crontab(hour=0, minute=0, day_of_week='saturday')
    'check_expired_order': {  # example: 'file-backup'
        'task': 'order.tasks.check_expired_order',  # example: 'files.tasks.cleanup'
        'schedule': timedelta(minutes=5),
    },
    'order_point_to_seller_account':{
        'task': 'order.tasks.order_point_to_seller_account',  # example: 'files.tasks.cleanup'
        'schedule': timedelta(hours=1),
    },
    'check_should_checkin_order':{
        'task': 'order.tasks.check_should_checkin_order',  # example: 'files.tasks.cleanup'
        'schedule': timedelta(hours=1),
    },
    'check_should_tag_checkout_order':{
        'task':'order.tasks.check_should_tag_checkout_order',
        'schedule':timedelta(hours=1)
    },
    'check_should_tag_checkin_order':{
        'task': 'order.tasks.check_should_tag_checkin_order',  # example: 'files.tasks.cleanup'
        'schedule': timedelta(hours=1),
    }

}


# Application definition
ROOT_URLCONF = 'chaolifeProject.urls'

#warn 这样做会节省宽带 但是会降低性能
USE_ETAGS = True

INSTALLED_APPS = [
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',#它将确保为你安装的应用中的每个Django模型创建3个默认的权限- add 、changed、delete
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'redis_cache',
    'rest_framework',
    'dynamic_rest',
    'grappelli',
    'grappelli.dashboard',
    'authtoken', #authen
    'guardian', # 对象权限控制
    'djcelery',
    'kombu.transport.django',
    'account', # 用户账号
    'hotel', # 酒店
    'sms',
    'pay', # 积分充值，
    'order', #订单处理
    'git_hook', # git hook 用于网站部署
    'message', # 消息推送，短信通知
    'chaolife', # 核心 ，待分离
    'devutils', # 开发帮助
    'chaolifeWeb', # html网站
]


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',#它向每个接受到的HttpRequeset对象添加user属性，表示当前登入的用户
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.MobileAppMiddleware',
]
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chaolifeProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
from chaolifeProject import dbconfig
DATABASES = dbconfig.get_config(testing=True).DATABASES

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators



# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

USE_I18N = True

USE_L10N = True

INTERNAL_IPS = ('127.0.0.1',)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/



# 是否最后可以 不加 splash
APPEND_SLASH = True

AUTH_USER_MODEL = 'account.User'

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# session setting
SESSION_COOKIE_AGE = 365*24*60*60


# 缓存系统
CACHES = {
'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'common_cache_table',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 2000
        }
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','debug_log'+str(datetime.datetime.today().date())+'.log'), #或者直接写路径：'c:\logs\all.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\request.log''
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\script.log'
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': { # 脚本专用日志
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

DEFAULT_API_VERSION = '0.1'
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
          'authtoken.authentication.BasicAuthentication',
          'authtoken.authentication.TokenAuthentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES':(
    ),
    'DEFAULT_THROTTLE_RATES': {
        'registrationEmsThrottle': '5/day',
    },
    'DEFAULT_PAGINATION_CLASS': 'chaolife.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 5,
    'EXCEPTION_HANDLER' : 'chaolife.utils.exceptionhandler.exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'common.utils.versioning.HttpHeaderVersioning',
    'DEFAULT_VERSION':DEFAULT_API_VERSION
}


DYNAMIC_REST = {
    # DEBUG: enable/disable internal debugging
    'DEBUG': True,

    # ENABLE_BROWSABLE_API: enable/disable the browsable API.
    # It can be useful to disable it in production.
    'ENABLE_BROWSABLE_API': True,

    # ENABLE_LINKS: enable/disable relationship links
    'ENABLE_LINKS': False,

    # ENABLE_SERIALIZER_CACHE: enable/disable caching of related serializers
    'ENABLE_SERIALIZER_CACHE': True,

    # ENABLE_SERIALIZER_OPTIMIZATIONS: enable/disable representation speedups
    'ENABLE_SERIALIZER_OPTIMIZATIONS': True,

    # DEFER_MANY_RELATIONS: automatically defer many-relations, unless
    # `deferred=False` is explicitly set on the field.
    'DEFER_MANY_RELATIONS': False,

    # MAX_PAGE_SIZE: global setting for max page size.
    # Can be overriden at the viewset level.
    'MAX_PAGE_SIZE': None,

    # PAGE_QUERY_PARAM: global setting for the pagination query parameter.
    # Can be overriden at the viewset level.
    'PAGE_QUERY_PARAM': 'page',

    # PAGE_SIZE: global setting for page size.
    # Can be overriden at the viewset level.
    'PAGE_SIZE': True,

    # PAGE_SIZE_QUERY_PARAM: global setting for the page size query parameter.
    # Can be overriden at the viewset level.
    'PAGE_SIZE_QUERY_PARAM': 'per_page',

    # ADDITIONAL_PRIMARY_RESOURCE_PREFIX: String to prefix additional
    # instances of the primary resource when sideloading.
    'ADDITIONAL_PRIMARY_RESOURCE_PREFIX': '+',

    # Enables host-relative links.  Only compatible with resources registered
    # through the dynamic router.  If a resource doesn't have a canonical
    # path registered, links will default back to being resource-relative urls
    'ENABLE_HOST_RELATIVE_LINKS': True,
    'DEFAULT_PAGINATION_CLASS': 'chaolife.pagination.StandardResultsSetPagination',
}

# REST_FRAMEWORK_CACHE　SETTING
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_ERRORS': False  #不cache error的情况
}


#邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.exmail.qq.com'                   #SMTP地址
EMAIL_PORT = 25                                 #SMTP端口
EMAIL_HOST_USER = 'chaomengshidai@agesd.com'           #自己的邮箱名
EMAIL_HOST_PASSWORD = 'gl123CMSD'           #自己的邮箱密码
EMAIL_SUBJECT_PREFIX = '项目开发'            #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                             #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false



FILE_UPLOAD_MAX_MEMORY_SIZE = 10621440

# 七牛文件系统设置
QINIU_ACCESS_KEY = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
QINIU_SECRET_KEY = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'
QINIU_BUCKET_NAME = 'hotelbook'
QINIU_BUCKET_DOMAIN = 'qiniu.agesd.com'
QINIU_SECURE_URL = False
DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'
# STATICFILES_STORAGE ='qiniustorage.backends.QiniuStaticStorage'

REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60



# 货币配置
import moneyed
DEFAULT_CURRENCY = 'CNY'