from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'list/([a-zA-Z\w\d\-\_]+)', views.list),
    url(r'edit/([a-zA-Z\w\d\-\_]+)', views.edit),
    url(r'detail/([a-zA-Z\w\d\-\_]+)', views.detail),
    url(r'add/([a-zA-Z\w\d\-\_]+)', views.add),
    url(r"show_qrcode", views.show_qrcode),
    url(r"get_qrcode", views.get_qrcode),
    url(r"scan_qrcode", views.scan_qrcode),
    url(r"decode_qrcode", views.decode_qrcode),
    url(r'login/', views.user_login),
    url(r'login', views.user_login),
    url(r'logout/', views.user_logout),
]
