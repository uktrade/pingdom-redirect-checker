from django.urls import re_path
from check_redirects import views

urlpatterns = [
    re_path(r'^$', views.url_search_results, name='url_search_result'),
    re_path(r'logs', views.logs, name='logs'),
    #url(r'scan', views.scan, name='scan'),
]
