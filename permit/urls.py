from django.urls import path
from .views import permit, print_permit, permit_detail, generate_permit_pdf
urlpatterns = [
    path('tp/', permit, name='transport-permit-view'),
    path("print/<pk>/", print_permit, name='print-permit'),
    path('detail/<pk>/', permit_detail, name='permit-detail'),
    path('hp/pdf/', generate_permit_pdf, name='harvest-permit-pdf')
]
