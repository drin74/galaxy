from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from .repositories import (
    GalaxyRepository,
    PlanetRepository,
    StarRepository,
    StatisticsRepository,
)

PLANETS_PER_PAGE = 10


def home(request):
    query = request.GET.get("q", "").strip()
    galaxy_type = request.GET.get("type", "").strip()
    ordering = request.GET.get("sort", "name").strip()

    galaxy_repo = GalaxyRepository()

    context = {
        "galaxies": galaxy_repo.list_with_counts(
            query=query,
            galaxy_type=galaxy_type,
            ordering=ordering,
        ),
        "query": query,
        "active_type": galaxy_type,
        "type_filters": galaxy_repo.type_filters(galaxy_type),
        "sort_options": galaxy_repo.ordering_options(ordering),
        "stats": StatisticsRepository().overview(),
        "spectral": StarRepository().spectral_distribution(),
        "habitable_planets": PlanetRepository().habitable(limit=4),
        "has_filters": bool(query or galaxy_type),
    }

    return render(request, "cosmos/home.html", context)


def galaxy_detail(request, pk):
    galaxy_repo = GalaxyRepository()
    galaxy = galaxy_repo.get_detail(pk)

    if galaxy is None:
        raise Http404("Галактика не найдена")

    query = request.GET.get("q", "").strip()
    spectral_class = request.GET.get("class", "").strip()
    ordering = request.GET.get("sort", "name").strip()

    star_repo = StarRepository()

    context = {
        "galaxy": galaxy,
        "stars": star_repo.list_by_galaxy(
            pk,
            query=query,
            spectral_class=spectral_class,
            ordering=ordering,
        ),
        "query": query,
        "active_class": spectral_class,
        "spectral_filters": star_repo.spectral_filters(
            spectral_class,
            galaxy_pk=pk,
        ),
        "sort_options": star_repo.ordering_options(ordering),
        "spectral": star_repo.spectral_distribution(galaxy_pk=pk),
        "has_filters": bool(query or spectral_class),
    }

    return render(request, "cosmos/galaxy_detail.html", context)


def planets(request):
    query = request.GET.get("q", "").strip()
    life = request.GET.get("life", "").strip()
    planet_type = request.GET.get("type", "").strip()
    ordering = request.GET.get("sort", "name").strip()

    has_life = {"yes": True, "no": False}.get(life)

    repo = PlanetRepository()
    queryset = repo.list_filtered(
        query=query,
        has_life=has_life,
        planet_type=planet_type,
        ordering=ordering,
    )

    paginator = Paginator(queryset, PLANETS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    life_counts = repo.life_counts()
    life_filters = [
        {
            "code": "",
            "label": "Все",
            "count": life_counts["yes"] + life_counts["no"],
            "active": not life,
        },
        {
            "code": "yes",
            "label": "С возможной жизнью",
            "count": life_counts["yes"],
            "active": life == "yes",
        },
        {
            "code": "no",
            "label": "Без жизни",
            "count": life_counts["no"],
            "active": life == "no",
        },
    ]

    context = {
        "planets": page_obj.object_list,
        "page_obj": page_obj,
        "total": paginator.count,
        "query": query,
        "life": life,
        "active_type": planet_type,
        "life_filters": life_filters,
        "type_filters": repo.type_filters(planet_type),
        "sort_options": repo.ordering_options(ordering),
        "records": repo.records(),
        "stats": StatisticsRepository().overview(),
        "has_filters": bool(query or life or planet_type),
    }

    return render(request, "cosmos/planets.html", context)


def star_detail(request, pk):
    star_repo = StarRepository()
    star = star_repo.get_detail(pk)

    if star is None:
        raise Http404("Звезда не найдена")

    context = {
        "star": star,
        "planets": star.planets.all(),
        "siblings": star_repo.siblings(star),
    }

    return render(request, "cosmos/star_detail.html", context)


def planet_detail(request, pk):
    repo = PlanetRepository()
    planet = repo.get_detail(pk)

    if planet is None:
        raise Http404("Планета не найдена")

    context = {
        "planet": planet,
        "siblings": repo.siblings(planet, limit=4),
    }

    return render(request, "cosmos/planet_detail.html", context)
