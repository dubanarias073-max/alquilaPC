from django.urls import path

from . import views

app_name = "liquidacion"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("liquidar/", views.liquidar, name="liquidar"),
    path("consultar/", views.consultar, name="consultar"),
    path("servicio/<int:numero>/", views.recibo, name="recibo"),
]
