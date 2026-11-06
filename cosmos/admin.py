from django.contrib import admin

from .models import Galaxy, Planet, Star


class StarInline(admin.TabularInline):
    model = Star
    extra = 0
    fields = ("name", "spectral_class", "temperature_k", "mass_solar")
    show_change_link = True


@admin.register(Galaxy)
class GalaxyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "galaxy_type",
        "distance_ly",
        "diameter_ly",
        "age_mln_years",
    )
    list_filter = ("galaxy_type",)
    search_fields = ("name", "description")
    inlines = [StarInline]


class PlanetInline(admin.TabularInline):
    model = Planet
    extra = 0
    fields = (
        "name",
        "planet_type",
        "radius_km",
        "distance_au",
        "has_life",
    )
    show_change_link = True


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "galaxy",
        "spectral_class",
        "temperature_k",
        "mass_solar",
    )
    list_filter = ("galaxy", "spectral_class")
    search_fields = ("name", "galaxy__name")
    list_select_related = ("galaxy",)
    inlines = [PlanetInline]


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "planet_type",
        "star",
        "radius_km",
        "distance_au",
        "has_life",
        "discovery_year",
    )
    list_filter = ("has_life", "planet_type", "star__galaxy")
    search_fields = ("name", "star__name", "star__galaxy__name")
    list_select_related = ("star", "star__galaxy")
    autocomplete_fields = ("star",)
