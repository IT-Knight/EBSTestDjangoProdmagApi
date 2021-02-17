=====
Commerce
=====

Commerce is a Django reusable app.

Quick start
-----------

1. Go to directory of commerce.tar.gz and run "pip install commerce.tar.gz" to install the app into your virtual enviroment of Django project

2. Config the settings.py like this::

from datetime import timedelta


    INSTALLED_APPS = [
        ...
    'commerce',
    'rest_framework',
    'drf_yasg',
    ]

    AUTH_USER_MODEL = 'commerce.User'

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],

    }

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Auth Token JWT': {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                }
            },
        }

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    }


3. Include the app URLconf in your project urls.py like this::

    path('', include('commerce.urls')),

4. Run ``python manage.py makemigrations` and ``python manage.py migrate`` 
   (fix simple errors if any)

5. Start the development server

6. Visit http://127.0.0.1:8000 to use the application
