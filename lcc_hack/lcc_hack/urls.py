from django.conf.urls import url
from django.contrib import admin
from lcc import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/', views.index, name='index'),
    url(r'^add_lcc/', views.add_lcc, name='add-lcc'),
]
