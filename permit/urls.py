from django.urls import path

from .views import (create_hp_view, create_tp_view, edit_tp_permit,
                    generate_tpermit_pdf, hp_list_view, load_district,
                    permit_detail, print_permit, tp_permit,
                    transport_permit_single_view)

urlpatterns = [
    path('tp/', tp_permit, name='transport-permit-view'),
    path("print/<pk>/", print_permit, name='print-permit'),
    path('detail/<pk>/', permit_detail, name='permit-detail'),
    path('tp/pdf/<pk>/<code>/', generate_tpermit_pdf,
         name='transport-permit-print'),
    path('hp/list/', hp_list_view, name='hp-view'),
    path('hp/new/', create_hp_view, name='create-hp-view'),
    path('ajax/load-districts/', load_district, name='ajax-load-districts'),
    path('tp/new/', create_tp_view, name='tp-create-view'),
    path('tp/view/<pk>/', transport_permit_single_view, name='tp-single-view'),
    path('tp/edit/<pk>/', edit_tp_permit, name='edit-tp-view')
]
