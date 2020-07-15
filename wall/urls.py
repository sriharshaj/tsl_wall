from django.urls import path
from django.conf.urls import url, include

from wall.views import current_user, PostView, UserView

urlpatterns = [
    path('current_user/', current_user, name='current-user'),
    url(r'^posts/', PostView.as_view(), name='post-list'),
    url(r'^users/', UserView.as_view(), name='user-list')
]
