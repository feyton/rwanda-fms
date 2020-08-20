from django.urls import path

from .views import (create_tp_view, dashboard_summary, edit_tp_permit,
                    generate_tpermit_pdf, load_district, permit_detail,
                    print_permit, tp_permit, transport_permit_single_view)

urlpatterns = [
    path('tp/', tp_permit, name='transport-permit-view'),
    path("print/<pk>/", print_permit, name='print-permit'),
    path('detail/<pk>/', permit_detail, name='permit-detail'),
    path('tp/pdf/<pk>/<code>/', generate_tpermit_pdf,
         name='transport-permit-print'),
    path('ajax/load-districts/', load_district, name='ajax-load-districts'),
    path('tp/new/', create_tp_view, name='tp-create-view'),
    path('tp/view/<pk>/', transport_permit_single_view, name='tp-single-view'),
    path('tp/edit/<pk>/', edit_tp_permit, name='edit-tp-view'),
    path('dashboard/summary/api/', dashboard_summary, name='dashboard-summary')
]
