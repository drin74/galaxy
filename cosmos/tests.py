from django.test import TestCase
from django.urls import reverse

from .models import Galaxy, Planet, Star
from .repositories import (
    GalaxyRepository,
    PlanetRepository,
    StarRepository,
    StatisticsRepository,
)


class RepositoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.milky = Galaxy.objects.create(
            name="Test Galaxy",
            galaxy_type=Galaxy.Types.SPIRAL,
            distance_ly=100,
            description="Наша тестовая галактика",
        )
        cls.far = Galaxy.objects.create(
            name="Far Galaxy",
            galaxy_type=Galaxy.Types.ELLIPTICAL,
            distance_ly=900,
        )
        cls.sun = Star.objects.create(
            galaxy=cls.milky,
            name="Test Star",
            spectral_class=Star.SpectralClass.G,
            temperature_k=6000,
            mass_solar=1.0,
        )
        cls.earth = Planet.objects.create(
            star=cls.sun,
            name="Test Earth",
            planet_type=Planet.Types.TERRESTRIAL,
            radius_km=6000,
            distance_au=1.0,
            has_life=True,
        )
        cls.giant = Planet.objects.create(
            star=cls.sun,
            name="Test Giant",
            planet_type=Planet.Types.GAS_GIANT,
            radius_km=60000,
            distance_au=5.0,
        )

    def test_galaxy_counts(self):
        galaxies = GalaxyRepository().list_with_counts()
        milky = next(item for item in galaxies if item.pk == self.milky.pk)
        self.assertEqual(milky.star_count, 1)
        self.assertEqual(milky.planet_count, 2)

    def test_galaxy_filter_and_search(self):
        repo = GalaxyRepository()
        self.assertEqual(repo.list_with_counts(galaxy_type="elliptical").count(), 1)
        self.assertEqual(repo.list_with_counts(query="тестовая").count(), 1)

    def test_galaxy_ordering_by_distance(self):
        galaxies = list(GalaxyRepository().list_with_counts(ordering="distance"))
        self.assertEqual(galaxies[0], self.milky)

    def test_type_filters_hide_empty_types(self):
        filters = GalaxyRepository().type_filters()
        codes = [item["code"] for item in filters]
        self.assertIn("spiral", codes)
        self.assertNotIn("irregular", codes)

    def test_planet_filters(self):
        repo = PlanetRepository()
        self.assertEqual(repo.list_filtered(has_life=True).count(), 1)
        self.assertEqual(repo.list_filtered(planet_type="gas_giant").count(), 1)
        self.assertEqual(repo.list_filtered(query="Test Star").count(), 2)

    def test_planet_ordering_by_radius(self):
        planets = list(PlanetRepository().list_filtered(ordering="radius_desc"))
        self.assertEqual(planets[0], self.giant)

    def test_records(self):
        records = PlanetRepository().records()
        self.assertEqual(records["largest"], self.giant)
        self.assertEqual(records["smallest"], self.earth)

    def test_statistics_overview(self):
        stats = StatisticsRepository().overview()
        self.assertEqual(stats["galaxies"], 2)
        self.assertEqual(stats["stars"], 1)
        self.assertEqual(stats["planets"], 2)
        self.assertEqual(stats["habitable"], 1)
        self.assertEqual(stats["habitable_share"], 50)

    def test_spectral_distribution(self):
        spectral = StarRepository().spectral_distribution()
        self.assertEqual(spectral["total"], 1)
        self.assertEqual(spectral["rows"][4]["code"], "G")
        self.assertEqual(spectral["rows"][4]["count"], 1)


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.galaxy = Galaxy.objects.create(
            name="View Galaxy",
            galaxy_type=Galaxy.Types.SPIRAL,
            distance_ly=42,
        )
        cls.star = Star.objects.create(
            galaxy=cls.galaxy,
            name="View Star",
            spectral_class=Star.SpectralClass.M,
            temperature_k=3200,
        )
        cls.planet = Planet.objects.create(
            star=cls.star,
            name="View Planet",
            planet_type=Planet.Types.SUPER_EARTH,
            radius_km=7000,
            has_life=True,
        )

    def test_home_page(self):
        response = self.client.get(reverse("cosmos:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Galaxy")

    def test_planets_page(self):
        response = self.client.get(reverse("cosmos:planets"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Planet")

    def test_planets_filter_by_life(self):
        response = self.client.get(reverse("cosmos:planets"), {"life": "no"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ничего не найдено")
        self.assertNotContains(response, '<td data-label="Планета">')

    def test_galaxy_detail_page(self):
        response = self.client.get(
            reverse("cosmos:galaxy_detail", args=[self.galaxy.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Star")

    def test_star_detail_page(self):
        response = self.client.get(
            reverse("cosmos:star_detail", args=[self.star.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Planet")

    def test_planet_detail_page(self):
        response = self.client.get(
            reverse("cosmos:planet_detail", args=[self.planet.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Star")

    def test_missing_objects_return_404(self):
        for name in ("cosmos:galaxy_detail", "cosmos:star_detail", "cosmos:planet_detail"):
            response = self.client.get(reverse(name, args=[999999]))
            self.assertEqual(response.status_code, 404)
