from django.core.management.base import BaseCommand

from cosmos.models import Galaxy, Planet, Star

GALAXIES = [
    {
        "name": "Млечный Путь",
        "galaxy_type": Galaxy.Types.SPIRAL,
        "distance_ly": 0,
        "diameter_ly": 105_700,
        "age_mln_years": 13_600,
        "description": (
            "Наш дом. Спиральная галактика с перемычкой, в которой находится "
            "Солнечная система. Содержит от 100 до 400 миллиардов звёзд."
        ),
    },
    {
        "name": "Андромеда (M31)",
        "galaxy_type": Galaxy.Types.SPIRAL,
        "distance_ly": 2_537_000,
        "diameter_ly": 220_000,
        "age_mln_years": 10_000,
        "description": (
            "Ближайшая крупная спиральная галактика к Млечному Пути. Через "
            "4,5 миллиарда лет столкнётся с нашей галактикой."
        ),
    },
    {
        "name": "Треугольник (M33)",
        "galaxy_type": Galaxy.Types.SPIRAL,
        "distance_ly": 2_730_000,
        "diameter_ly": 60_000,
        "age_mln_years": 13_000,
        "description": (
            "Третья по величине галактика Местной группы. Видна с Земли как "
            "туманное пятно в созвездии Треугольника."
        ),
    },
    {
        "name": "Большое Магелланово Облако",
        "galaxy_type": Galaxy.Types.IRREGULAR,
        "distance_ly": 163_000,
        "diameter_ly": 14_000,
        "age_mln_years": 13_000,
        "description": (
            "Галактика-спутник Млечного Пути. Видна невооружённым глазом в "
            "южном полушарии и содержит область звёздообразования Тарантул."
        ),
    },
    {
        "name": "Водоворот (M51)",
        "galaxy_type": Galaxy.Types.SPIRAL,
        "distance_ly": 23_000_000,
        "diameter_ly": 76_000,
        "age_mln_years": 400,
        "description": (
            "Классическая спиральная галактика, взаимодействующая со своим "
            "компаньоном NGC 5195. Эталонный пример спиральной структуры."
        ),
    },
    {
        "name": "Сомбреро (M104)",
        "galaxy_type": Galaxy.Types.LENTICULAR,
        "distance_ly": 29_300_000,
        "diameter_ly": 49_000,
        "age_mln_years": 13_250,
        "description": (
            "Линзовидная галактика со знаменитым тёмным пылевым диском, "
            "который напоминает поля шляпы сомбреро."
        ),
    },
    {
        "name": "M87",
        "galaxy_type": Galaxy.Types.ELLIPTICAL,
        "distance_ly": 53_500_000,
        "diameter_ly": 132_000,
        "age_mln_years": 13_250,
        "description": (
            "Гигантская эллиптическая галактика в центре скопления Девы. "
            "Здесь находится сверхмассивная чёрная дыра M87*, снятая телескопом EHT."
        ),
    },
    {
        "name": "Колесо Телеги",
        "galaxy_type": Galaxy.Types.IRREGULAR,
        "distance_ly": 500_000_000,
        "diameter_ly": 150_000,
        "age_mln_years": 440,
        "description": (
            "Кольцевая галактика, образовавшаяся после столкновения двух "
            "галактик. Яркое кольцо звёздообразования окружает её центр."
        ),
    },
]

STARS = [
    {
        "galaxy": "Млечный Путь",
        "name": "Солнце",
        "spectral_class": Star.SpectralClass.G,
        "temperature_k": 5_778,
        "mass_solar": 1.0,
    },
    {
        "galaxy": "Млечный Путь",
        "name": "Проксима Центавра",
        "spectral_class": Star.SpectralClass.M,
        "temperature_k": 3_042,
        "mass_solar": 0.12,
    },
    {
        "galaxy": "Млечный Путь",
        "name": "Сириус A",
        "spectral_class": Star.SpectralClass.A,
        "temperature_k": 9_940,
        "mass_solar": 2.06,
    },
    {
        "galaxy": "Млечный Путь",
        "name": "Бетельгейзе",
        "spectral_class": Star.SpectralClass.M,
        "temperature_k": 3_600,
        "mass_solar": 16.5,
    },
    {
        "galaxy": "Млечный Путь",
        "name": "TRAPPIST-1",
        "spectral_class": Star.SpectralClass.M,
        "temperature_k": 2_566,
        "mass_solar": 0.09,
    },
    {
        "galaxy": "Млечный Путь",
        "name": "Kepler-186",
        "spectral_class": Star.SpectralClass.M,
        "temperature_k": 3_755,
        "mass_solar": 0.54,
    },
    {
        "galaxy": "Млечный Путь",
        "name": "Вега",
        "spectral_class": Star.SpectralClass.A,
        "temperature_k": 9_602,
        "mass_solar": 2.14,
    },
    {
        "galaxy": "Андромеда (M31)",
        "name": "Альферац",
        "spectral_class": Star.SpectralClass.B,
        "temperature_k": 13_800,
        "mass_solar": 3.6,
    },
    {
        "galaxy": "Андромеда (M31)",
        "name": "Мирах",
        "spectral_class": Star.SpectralClass.M,
        "temperature_k": 3_800,
        "mass_solar": 1.2,
    },
    {
        "galaxy": "Большое Магелланово Облако",
        "name": "R136a1",
        "spectral_class": Star.SpectralClass.O,
        "temperature_k": 46_000,
        "mass_solar": 215.0,
    },
]

PLANETS = [

    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Меркурий",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 2_440,
        "mass_earth": 0.055,
        "distance_au": 0.39,
        "orbital_period_days": 88.0,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Венера",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 6_052,
        "mass_earth": 0.815,
        "distance_au": 0.72,
        "orbital_period_days": 224.7,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Земля",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 6_371,
        "mass_earth": 1.0,
        "distance_au": 1.0,
        "orbital_period_days": 365.25,
        "has_life": True,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Марс",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 3_390,
        "mass_earth": 0.107,
        "distance_au": 1.52,
        "orbital_period_days": 687.0,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Юпитер",
        "planet_type": Planet.Types.GAS_GIANT,
        "radius_km": 69_911,
        "mass_earth": 317.8,
        "distance_au": 5.2,
        "orbital_period_days": 4_332.6,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Сатурн",
        "planet_type": Planet.Types.GAS_GIANT,
        "radius_km": 58_232,
        "mass_earth": 95.2,
        "distance_au": 9.58,
        "orbital_period_days": 10_759.0,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Уран",
        "planet_type": Planet.Types.ICE_GIANT,
        "radius_km": 25_362,
        "mass_earth": 14.5,
        "distance_au": 19.2,
        "orbital_period_days": 30_687.0,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Солнце",
        "name": "Нептун",
        "planet_type": Planet.Types.ICE_GIANT,
        "radius_km": 24_622,
        "mass_earth": 17.1,
        "distance_au": 30.05,
        "orbital_period_days": 60_190.0,
    },

    {
        "galaxy": "Млечный Путь",
        "star": "Проксима Центавра",
        "name": "Проксима b",
        "planet_type": Planet.Types.SUPER_EARTH,
        "radius_km": 7_160,
        "mass_earth": 1.27,
        "distance_au": 0.0485,
        "orbital_period_days": 11.2,
        "has_life": True,
        "discovery_year": 2016,
    },

    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1b",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 7_100,
        "mass_earth": 0.85,
        "distance_au": 0.0115,
        "orbital_period_days": 1.51,
        "discovery_year": 2016,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1c",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 7_100,
        "mass_earth": 1.38,
        "distance_au": 0.0158,
        "orbital_period_days": 2.42,
        "discovery_year": 2016,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1d",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 5_100,
        "mass_earth": 0.39,
        "distance_au": 0.0223,
        "orbital_period_days": 4.05,
        "discovery_year": 2016,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1e",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 5_800,
        "mass_earth": 0.69,
        "distance_au": 0.0293,
        "orbital_period_days": 6.1,
        "has_life": True,
        "discovery_year": 2017,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1f",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 6_700,
        "mass_earth": 0.91,
        "distance_au": 0.0385,
        "orbital_period_days": 9.21,
        "discovery_year": 2017,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1g",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 7_300,
        "mass_earth": 1.15,
        "distance_au": 0.0469,
        "orbital_period_days": 12.35,
        "discovery_year": 2017,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "TRAPPIST-1",
        "name": "TRAPPIST-1h",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 5_100,
        "mass_earth": 0.33,
        "distance_au": 0.0619,
        "orbital_period_days": 18.77,
        "discovery_year": 2017,
    },

    {
        "galaxy": "Млечный Путь",
        "star": "Kepler-186",
        "name": "Kepler-186b",
        "planet_type": Planet.Types.SUPER_EARTH,
        "radius_km": 7_900,
        "mass_earth": 1.5,
        "distance_au": 0.0343,
        "orbital_period_days": 3.89,
        "discovery_year": 2014,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Kepler-186",
        "name": "Kepler-186c",
        "planet_type": Planet.Types.SUPER_EARTH,
        "radius_km": 8_300,
        "mass_earth": 2.0,
        "distance_au": 0.045,
        "orbital_period_days": 7.27,
        "discovery_year": 2014,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Kepler-186",
        "name": "Kepler-186d",
        "planet_type": Planet.Types.SUPER_EARTH,
        "radius_km": 8_700,
        "mass_earth": 2.4,
        "distance_au": 0.078,
        "orbital_period_days": 13.34,
        "discovery_year": 2014,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Kepler-186",
        "name": "Kepler-186e",
        "planet_type": Planet.Types.SUPER_EARTH,
        "radius_km": 8_300,
        "mass_earth": 2.0,
        "distance_au": 0.11,
        "orbital_period_days": 22.4,
        "discovery_year": 2014,
    },
    {
        "galaxy": "Млечный Путь",
        "star": "Kepler-186",
        "name": "Kepler-186f",
        "planet_type": Planet.Types.TERRESTRIAL,
        "radius_km": 7_300,
        "mass_earth": 1.4,
        "distance_au": 0.432,
        "orbital_period_days": 129.9,
        "has_life": True,
        "discovery_year": 2014,
    },
]


class Command(BaseCommand):
    help = "Заполняет базу примерами данных о Вселенной"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Удалить существующие данные перед загрузкой",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            Planet.objects.all().delete()
            Star.objects.all().delete()
            Galaxy.objects.all().delete()
            self.stdout.write(self.style.WARNING("Старые данные удалены."))

        galaxies = {}
        for data in GALAXIES:
            galaxy, _ = Galaxy.objects.update_or_create(
                name=data["name"],
                defaults={
                    "galaxy_type": data["galaxy_type"],
                    "distance_ly": data["distance_ly"],
                    "diameter_ly": data["diameter_ly"],
                    "age_mln_years": data["age_mln_years"],
                    "description": data["description"],
                },
            )
            galaxies[galaxy.name] = galaxy

        stars = {}
        for data in STARS:
            star, _ = Star.objects.update_or_create(
                galaxy=galaxies[data["galaxy"]],
                name=data["name"],
                defaults={
                    "spectral_class": data["spectral_class"],
                    "temperature_k": data["temperature_k"],
                    "mass_solar": data["mass_solar"],
                },
            )
            stars[(data["galaxy"], star.name)] = star

        for data in PLANETS:
            Planet.objects.update_or_create(
                star=stars[(data["galaxy"], data["star"])],
                name=data["name"],
                defaults={
                    "planet_type": data["planet_type"],
                    "radius_km": data.get("radius_km"),
                    "mass_earth": data.get("mass_earth"),
                    "distance_au": data.get("distance_au"),
                    "orbital_period_days": data.get("orbital_period_days"),
                    "has_life": data.get("has_life", False),
                    "discovery_year": data.get("discovery_year"),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Данные загружены: "
                f"{len(GALAXIES)} галактик, "
                f"{len(STARS)} звёзд, "
                f"{len(PLANETS)} планет."
            )
        )
