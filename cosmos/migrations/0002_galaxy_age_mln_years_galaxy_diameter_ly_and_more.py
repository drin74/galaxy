from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cosmos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galaxy',
            name='age_mln_years',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст, млн лет'),
        ),
        migrations.AddField(
            model_name='galaxy',
            name='diameter_ly',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Диаметр, световые годы'),
        ),
        migrations.AddField(
            model_name='planet',
            name='distance_au',
            field=models.FloatField(blank=True, null=True, verbose_name='Расстояние от звезды, а.е.'),
        ),
        migrations.AddField(
            model_name='planet',
            name='mass_earth',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса, M⊕'),
        ),
        migrations.AddField(
            model_name='planet',
            name='orbital_period_days',
            field=models.FloatField(blank=True, null=True, verbose_name='Период обращения, суток'),
        ),
        migrations.AddField(
            model_name='planet',
            name='planet_type',
            field=models.CharField(choices=[('terrestrial', 'Землеподобная'), ('super_earth', 'Суперземля'), ('gas_giant', 'Газовый гигант'), ('ice_giant', 'Ледяной гигант'), ('dwarf', 'Карликовая')], default='terrestrial', max_length=20, verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='star',
            name='mass_solar',
            field=models.FloatField(blank=True, null=True, verbose_name='Масса, M☉'),
        ),
    ]
