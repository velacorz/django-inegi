from django.urls import path
from .views import EstadoListView

urlpatterns = [
    path("geo/", EstadoListView.as_view(), name="geo-list"),
]
