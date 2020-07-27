from django.urls import path, include
from . import views
from permit.views import test_template

urlpatterns = [
    path('', views.home_view, name='home'),
    path('test/', test_template)
]
