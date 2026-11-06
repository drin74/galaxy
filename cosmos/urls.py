from django.urls import path

from . import views

app_name = "cosmos"

urlpatterns = [
    path("", views.home, name="home"),
    path("galaxy/<int:pk>/", views.galaxy_detail, name="galaxy_detail"),
    path("star/<int:pk>/", views.star_detail, name="star_detail"),
    path("planets/", views.planets, name="planets"),
    path("planet/<int:pk>/", views.planet_detail, name="planet_detail"),
]
