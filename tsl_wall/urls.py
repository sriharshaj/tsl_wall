from django.urls import path, include
from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api/', include('wall.urls')),
    path('api/token-auth/', obtain_jwt_token)
]
