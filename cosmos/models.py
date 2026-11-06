from django.db import models


class Galaxy(models.Model):
    class Types(models.TextChoices):
        SPIRAL = "spiral", "Спиральная"
        ELLIPTICAL = "elliptical", "Эллиптическая"
        IRREGULAR = "irregular", "Неправильная"
        LENTICULAR = "lenticular", "Линзовидная"

    name = models.CharField("Название", max_length=120, unique=True)
    galaxy_type = models.CharField(
        "Тип",
        max_length=20,
        choices=Types.choices,
        default=Types.SPIRAL,
    )
    distance_ly = models.PositiveIntegerField(
        "Расстояние, световые годы",
        null=True,
        blank=True,
    )
    diameter_ly = models.PositiveIntegerField(
        "Диаметр, световые годы",
        null=True,
        blank=True,
    )
    age_mln_years = models.PositiveIntegerField(
        "Возраст, млн лет",
        null=True,
        blank=True,
    )
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Галактика"
        verbose_name_plural = "Галактики"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Star(models.Model):
    class SpectralClass(models.TextChoices):
        O = "O", "O — очень горячая"
        B = "B", "B — горячая"
        A = "A", "A — белая"
        F = "F", "F — жёлто-белая"
        G = "G", "G — жёлтая"
        K = "K", "K — оранжевая"
        M = "M", "M — красная"

    galaxy = models.ForeignKey(
        Galaxy,
        on_delete=models.CASCADE,
        related_name="stars",
        verbose_name="Галактика",
    )
    name = models.CharField("Название", max_length=120)
    spectral_class = models.CharField(
        "Спектральный класс",
        max_length=1,
        choices=SpectralClass.choices,
        blank=True,
    )
    temperature_k = models.PositiveIntegerField(
        "Температура, K",
        null=True,
        blank=True,
    )
    mass_solar = models.FloatField(
        "Масса, M☉",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Звезда"
        verbose_name_plural = "Звёзды"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["galaxy", "name"],
                name="uniq_star_in_galaxy",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.galaxy.name})"


class Planet(models.Model):
    class Types(models.TextChoices):
        TERRESTRIAL = "terrestrial", "Землеподобная"
        SUPER_EARTH = "super_earth", "Суперземля"
        GAS_GIANT = "gas_giant", "Газовый гигант"
        ICE_GIANT = "ice_giant", "Ледяной гигант"
        DWARF = "dwarf", "Карликовая"

    star = models.ForeignKey(
        Star,
        on_delete=models.CASCADE,
        related_name="planets",
        verbose_name="Звезда",
    )
    name = models.CharField("Название", max_length=120)
    planet_type = models.CharField(
        "Тип",
        max_length=20,
        choices=Types.choices,
        default=Types.TERRESTRIAL,
    )
    radius_km = models.PositiveIntegerField(
        "Радиус, км",
        null=True,
        blank=True,
    )
    mass_earth = models.FloatField(
        "Масса, M⊕",
        null=True,
        blank=True,
    )
    distance_au = models.FloatField(
        "Расстояние от звезды, а.е.",
        null=True,
        blank=True,
    )
    orbital_period_days = models.FloatField(
        "Период обращения, суток",
        null=True,
        blank=True,
    )
    has_life = models.BooleanField("Возможна жизнь", default=False)
    discovery_year = models.PositiveSmallIntegerField(
        "Год открытия",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Планета"
        verbose_name_plural = "Планеты"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["star", "name"],
                name="uniq_planet_in_star",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.star.name})"
