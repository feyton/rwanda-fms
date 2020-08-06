from django.urls import path

from .views import (generate_permit_pdf, hp_list_view, permit, permit_detail,
                    print_permit, create_hp_view, load_district)

urlpatterns = [
    path('tp/', permit, name='transport-permit-view'),
    path("print/<pk>/", print_permit, name='print-permit'),
    path('detail/<pk>/', permit_detail, name='permit-detail'),
    path('hp/pdf/', generate_permit_pdf, name='harvest-permit-pdf'),
    path('hp/list/', hp_list_view, name='hp-view'),
    path('hp/new/', create_hp_view, name='create-hp-view'),
    path('ajax/load-districts/', load_district, name='ajax-load-districts')
]
