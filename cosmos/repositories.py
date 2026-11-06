from django.db.models import Count, F, Q

from .models import Galaxy, Planet, Star


class BaseRepository:
    model = None
    default_ordering = "name"
    ORDERINGS = {"name": ("name",)}
    ORDERING_LABELS = {"name": "По названию"}

    def count(self):
        return self.model.objects.count()

    def get_by_pk(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def _ordered(self, queryset, ordering):
        keys = self.ORDERINGS.get(
            ordering,
            self.ORDERINGS.get(self.default_ordering, ("name",)),
        )
        return queryset.order_by(*keys)

    def ordering_options(self, active="name"):
        if active not in self.ORDERINGS:
            active = self.default_ordering
        return [
            {"code": code, "label": label, "active": code == active}
            for code, label in self.ORDERING_LABELS.items()
        ]


class GalaxyRepository(BaseRepository):
    model = Galaxy

    ORDERINGS = {
        "name": ("name",),
        "stars": ("-star_count", "name"),
        "planets": ("-planet_count", "name"),
        "distance": (F("distance_ly").asc(nulls_last=True), "name"),
        "distance_desc": (F("distance_ly").desc(nulls_last=True), "name"),
    }
    ORDERING_LABELS = {
        "name": "По названию",
        "stars": "По числу звёзд",
        "planets": "По числу планет",
        "distance": "Сначала близкие",
        "distance_desc": "Сначала далёкие",
    }

    def list_with_counts(self, query="", galaxy_type="", ordering="name"):
        queryset = self.model.objects.annotate(
            star_count=Count("stars", distinct=True),
            planet_count=Count("stars__planets", distinct=True),
        )

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        if galaxy_type:
            queryset = queryset.filter(galaxy_type=galaxy_type)

        return self._ordered(queryset, ordering)

    def get_detail(self, pk):
        return (
            self.model.objects
            .annotate(
                star_count=Count("stars", distinct=True),
                planet_count=Count("stars__planets", distinct=True),
            )
            .filter(pk=pk)
            .first()
        )

    def type_filters(self, active=""):
        counts = dict(
            self.model.objects
            .values_list("galaxy_type")
            .annotate(total=Count("id"))
        )
        total = sum(counts.values())

        options = [
            {
                "code": "",
                "label": "Все",
                "count": total,
                "active": not active,
            }
        ]

        for code, label in self.model.Types.choices:
            count = counts.get(code, 0)
            if count == 0 and code != active:
                continue

            options.append(
                {
                    "code": code,
                    "label": label,
                    "count": count,
                    "active": code == active,
                }
            )

        return options


class StarRepository(BaseRepository):
    model = Star

    ORDERINGS = {
        "name": ("name",),
        "temperature": (F("temperature_k").desc(nulls_last=True), "name"),
        "mass": (F("mass_solar").desc(nulls_last=True), "name"),
    }
    ORDERING_LABELS = {
        "name": "По названию",
        "temperature": "По температуре",
        "mass": "По массе",
    }

    def list_by_galaxy(self, galaxy_pk, query="", spectral_class="", ordering="name"):
        queryset = (
            self.model.objects
            .filter(galaxy_id=galaxy_pk)
            .prefetch_related("planets")
        )

        if query:
            queryset = queryset.filter(name__icontains=query)

        if spectral_class:
            queryset = queryset.filter(spectral_class=spectral_class)

        return self._ordered(queryset, ordering)

    def get_detail(self, pk):
        return (
            self.model.objects
            .select_related("galaxy")
            .prefetch_related("planets")
            .filter(pk=pk)
            .first()
        )

    def siblings(self, star, limit=4):
        return (
            self.model.objects
            .filter(galaxy_id=star.galaxy_id)
            .exclude(pk=star.pk)
            .order_by("name")[:limit]
        )

    def spectral_filters(self, active="", galaxy_pk=None):
        queryset = self.model.objects
        if galaxy_pk is not None:
            queryset = queryset.filter(galaxy_id=galaxy_pk)

        counts = dict(
            queryset
            .exclude(spectral_class="")
            .values_list("spectral_class")
            .annotate(total=Count("id"))
        )
        total = sum(counts.values())

        options = [
            {
                "code": "",
                "label": "Все",
                "count": total,
                "active": not active,
            }
        ]

        for code, label in self.model.SpectralClass.choices:
            count = counts.get(code, 0)
            if count == 0 and code != active:
                continue

            options.append(
                {
                    "code": code,
                    "label": label.split(" — ")[0],
                    "count": count,
                    "active": code == active,
                }
            )

        return options

    def spectral_distribution(self, galaxy_pk=None):
        queryset = self.model.objects.exclude(spectral_class="")
        if galaxy_pk is not None:
            queryset = queryset.filter(galaxy_id=galaxy_pk)

        counts = dict(
            queryset
            .values_list("spectral_class")
            .annotate(total=Count("id"))
        )
        total = sum(counts.values())
        peak = max(counts.values(), default=0) or 1

        rows = []
        for code, label in self.model.SpectralClass.choices:
            count = counts.get(code, 0)
            name, _, description = label.partition(" — ")
            rows.append(
                {
                    "code": code,
                    "name": name,
                    "description": description,
                    "count": count,
                    "width": round(count / peak * 100),
                    "share": round(count / total * 100) if total else 0,
                }
            )

        return {"rows": rows, "total": total}


class PlanetRepository(BaseRepository):
    model = Planet

    ORDERINGS = {
        "name": ("name",),
        "radius": (F("radius_km").asc(nulls_last=True), "name"),
        "radius_desc": (F("radius_km").desc(nulls_last=True), "name"),
        "distance": (F("distance_au").asc(nulls_last=True), "name"),
        "year": (F("discovery_year").asc(nulls_last=True), "name"),
        "year_desc": (F("discovery_year").desc(nulls_last=True), "name"),
    }
    ORDERING_LABELS = {
        "name": "По названию",
        "radius": "Сначала маленькие",
        "radius_desc": "Сначала большие",
        "distance": "Ближе к звезде",
        "year": "Сначала старые открытия",
        "year_desc": "Сначала новые открытия",
    }

    def list_filtered(self, query="", has_life=None, planet_type="", ordering="name"):
        queryset = self.model.objects.select_related("star__galaxy")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(star__name__icontains=query)
                | Q(star__galaxy__name__icontains=query)
            )

        if has_life is True:
            queryset = queryset.filter(has_life=True)
        elif has_life is False:
            queryset = queryset.filter(has_life=False)

        if planet_type:
            queryset = queryset.filter(planet_type=planet_type)

        return self._ordered(queryset, ordering)

    def get_detail(self, pk):
        return (
            self.model.objects
            .select_related("star__galaxy")
            .filter(pk=pk)
            .first()
        )

    def type_filters(self, active=""):
        counts = dict(
            self.model.objects
            .values_list("planet_type")
            .annotate(total=Count("id"))
        )
        total = sum(counts.values())

        options = [
            {
                "code": "",
                "label": "Все типы",
                "count": total,
                "active": not active,
            }
        ]

        for code, label in self.model.Types.choices:
            count = counts.get(code, 0)
            if count == 0 and code != active:
                continue

            options.append(
                {
                    "code": code,
                    "label": label,
                    "count": count,
                    "active": code == active,
                }
            )

        return options

    def life_counts(self):
        return {
            "yes": self.model.objects.filter(has_life=True).count(),
            "no": self.model.objects.filter(has_life=False).count(),
        }

    def habitable(self, limit=4):
        return (
            self.model.objects
            .filter(has_life=True)
            .select_related("star__galaxy")
            .order_by("name")[:limit]
        )

    def siblings(self, planet, limit=4):
        return (
            self.model.objects
            .filter(star=planet.star)
            .exclude(pk=planet.pk)
            .select_related("star__galaxy")
            .order_by("name")[:limit]
        )

    def records(self):
        base = self.model.objects.select_related("star__galaxy")
        return {
            "largest": base.filter(radius_km__isnull=False).order_by("-radius_km").first(),
            "smallest": base.filter(radius_km__isnull=False).order_by("radius_km").first(),
            "farthest": base.filter(distance_au__isnull=False).order_by("-distance_au").first(),
            "oldest": base.filter(discovery_year__isnull=False).order_by("discovery_year").first(),
        }


class StatisticsRepository:
    def overview(self):
        galaxies = Galaxy.objects.count()
        stars = Star.objects.count()
        planets = Planet.objects.count()
        habitable = Planet.objects.filter(has_life=True).count()

        return {
            "galaxies": galaxies,
            "stars": stars,
            "planets": planets,
            "habitable": habitable,
            "habitable_share": round(habitable / planets * 100) if planets else 0,
            "stars_per_galaxy": round(stars / galaxies, 1) if galaxies else 0,
            "planets_per_star": round(planets / stars, 2) if stars else 0,
        }
