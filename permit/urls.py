from django.urls import path
from .views import permit, print_permit, permit_detail
urlpatterns = [
    path('', permit, name='transport-permit-view'),
    path("print/<pk>/", print_permit, name='print-permit'),
    path('detail/<pk>/', permit_detail, name='permit-detail')
]
