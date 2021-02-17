
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Poduct Magazine",
        default_version='v1',
        description='1. Register\n'
                    '2. Get Token\n'
                    '3. To use token: input "Bearer &lsaquo;token&rsaquo;" without quotes\n'
                    'Example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl9\n'
                    '4. To refresh token: input just the refresh token without "Bearer" and quotes\n\n'
                    'Access token lifetime: 30 minutes\n'
                    'Refresh token lifetime: 24 hours',
    ),
    public=True,
    validators=['ssv'],
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
