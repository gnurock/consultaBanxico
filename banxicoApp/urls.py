from django.urls import path
from .views import home,serie_tiie,serie_dolar

urlpatterns = [
    path("", home, name="home"),
    path('tiee/', serie_tiie, name='serie tiie'),
    path('dolar/', serie_dolar , name='serie_dolar'),
]
