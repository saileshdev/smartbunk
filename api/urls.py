from django.urls import path
from . import views

urlpatterns = [
    path('fetchAttendance/', views.fetch_attendance),
    path('createOrder/', views.create_order),
    path('verifySignature/', views.verify_signature),
]
