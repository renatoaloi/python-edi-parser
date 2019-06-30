"""
Django settings for edi project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qx%(q(t748+$@w3qsyb3hlw$wv3h_#^n!jx3y^jki3=lvq0ytx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# File layouts

EDI_LAYOUTS = [
    {
        'id': '1',
        'type': 'Remessa e/ou Retorno de Vendas',
        'layout': [
            {
                'registro': 'header',
                'regex': r'^00\d{8}\d{7}.{10}\d{3}\d{10}$',
                'positions': ( (1, 2), (3, 8), (11, 7), (18, 10), (28, 3), (31, 10), ),
                'formato': ( 'N', 'N', 'N', 'X', 'N', 'N', ),
                'obrigatorio': ( False, True, True, False, False, True, ),
                'custom_validation': ( None, 'Date', 'UniqueWithin30days', None, None, None ),
                'custom_action': ( None, None, 'SaveField', None, None, 'SaveField' )
            },
            {
                'registro': 'detalhe',
                'regex': r'^01\d{7}\d{19}.{6}\d{8}\d{1}\d{15}\d{3}\d{15}\d{15}\d{15}\d{15}\d{7}[0]{3}\d{10}.{30}\d{2}\d{8}\d{4}[0]{7}[0]{15}.{3}.{4}[ ]{11}.{19}\d{4}[ ]{2}$',
                'positions': ( (1, 2), (3, 7), (10, 19), (29, 6), (35, 8), (43, 1), (44, 15), (59, 3), (62, 15), (77, 15), (92, 15), (107, 15), (122, 7), (129, 3), (132, 10), (142, 30), (172, 2), (174, 8), (182, 4), (186, 7), (193, 15), (208, 4), (211, 4), (215, 11), (226, 19), (245, 4), (249, 2), ),
                'formato': ( 'N','N','N','X','N','N','N','N','N','N','N','N','N','N','N','X','N','N','X','N','N','X','X','X','X','N','X', ),
                'obrigatorio': ( False, True, True, False, True, True, True, True, True, False, False, True, True, False, True, False, False, False, True, False, False, False, False, False, False, False, False, ),
                'custom_validation': ( None, 'Unique', 'GreaterThanOrEqualTo16', None, 'Date', 'Distinct', None, None, None, None, None, None, 'SameAsHeader3', None, 'SameAsHeader6', None, None, None, None, None, None, None, None, None, None, None, None, ),
                'custom_action': ( None, None, None, None, None, None, 'SumField', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, )
            },
            {
                'registro': 'trailler',
                'regex': r'^99\d{7}\d{15}\d{15}\d{15}\d{8}.{188}$',
                'positions': ( (1, 2), (3, 7), (10, 15), (25, 15), (40, 15), (55, 8), (63, 188), ),
                'formato': ( 'N', 'N', 'N', 'N', 'N', 'N', 'X', ),
                'obrigatorio': ( False, True, True, False, False, False, False, ),
                'custom_validation': ( None, None, 'SumDetalhe7', None, None, None, None, ),
                'custom_action': ( None, None, None, None, None, None, None, )
            }
        ]
    }
]


# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flatparser',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edi.urls'

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

WSGI_APPLICATION = 'edi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')