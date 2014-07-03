# -*- coding: utf-8 -*-
# Django settings for tornado_dj project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tornado-db',                      # Or path to database file if using sqlite3.
        'USER': 'tornado-user',                      # Not used with sqlite3.
        'PASSWORD': '321',                  # Not used with sqlite3.
        'HOST': '192.168.56.101',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1


USE_I18N = True
USE_L10N = True
USE_TZ = True


MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'zglyn708wbkae7l3**6j^(#k397fc9r*a&amp;-)5np2so7geqbabe'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
)

ROOT_URLCONF = 'django_apps.urls'

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '', '../templates').replace('\\','/'),)
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '', '../dj_templates').replace('\\','/'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'south',
    'social_auth',

    'django_apps.dj_site',
    'django_apps.gamesapp',
    'django_apps.teamapp',
    'django_apps.userman'
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# FORCE_SCRIPT_NAME = '/dj'

###   SOCIAL-AUTH  #######################
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.disqus.DisqusBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Setup login URLs:
LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/register-user'
LOGIN_ERROR_URL    = '/login-error/'

#If a custom redirect URL is needed that must be different to LOGIN_URL, define the setting:
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/another-login-url/'

#A different URL could be defined for newly registered users:
# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'

#or for newly associated accounts:
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'

#or for account disconnections:
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'

#Users will be redirected to LOGIN_ERROR_URL in case of error or user cancellation on some backends. This URL can be override by this setting:
# SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'

#Configure authentication and association complete URL names to avoid possible clashes:
# SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
# SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

#Inactive users can be redirected to a different page if this setting is defined:
# SOCIAL_AUTH_INACTIVE_USER_URL = '...'

# It’s possible to override the used User model if needed:
# SOCIAL_AUTH_USER_MODEL = 'myapp.CustomUser'

# Used to build a default username if provider didn’t returned any useful value:
SOCIAL_AUTH_DEFAULT_USERNAME = 'social-anonym'

SOCIAL_AUTH_CREATE_USERS = True

# Перечислим pipeline, которые последовательно буду обрабатывать респонс
SOCIAL_AUTH_PIPELINE = (
    # Получает по backend и uid инстансы social_user и user
    'social_auth.backends.pipeline.social.social_auth_user',
    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
    'social_auth.backends.pipeline.associate.associate_by_email',
    # Пытается собрать правильный username, на основе уже имеющихся данных
    'social_auth.backends.pipeline.user.get_username',
    # Создает нового пользователя, если такого еще нет
    'social_auth.backends.pipeline.user.create_user',
    # Пытается связать аккаунты
    'social_auth.backends.pipeline.social.associate_user',
    # Получает и обновляет social_user.extra_data
    'social_auth.backends.pipeline.social.load_extra_data',
    # Обновляет инстанс user дополнительными данными с бекенда
    'social_auth.backends.pipeline.user.update_user_details'
)

from settings_local import *
