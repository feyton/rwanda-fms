from django.urls import path

from . import views as v

urlpatterns = [
    path('harvesting-permits', v.hp_list_view, name='hp-view'),
    path('create/permit/', v.create_hp_view, name='create-hp-view'),
    path('detail/<pk>/', v.HPermitDetailView.as_view(), name='harvesting_permit_detail')
]
