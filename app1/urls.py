from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.honsy),
    url(r'list/([a-zA-Z\w\d\-\_]+)', views.list),
    url(r'edit/([a-zA-Z\w\d\-\_]+)', views.edit),
    url(r'add/([a-zA-Z\w\d\-\_]+)', views.add),
    url(r'login/', views.user_login),
    url(r'login', views.user_login),
    url(r'logout/', views.user_logout),
]
