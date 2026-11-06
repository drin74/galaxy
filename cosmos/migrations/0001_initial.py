import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Galaxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название')),
                ('galaxy_type', models.CharField(choices=[('spiral', 'Спиральная'), ('elliptical', 'Эллиптическая'), ('irregular', 'Неправильная'), ('lenticular', 'Линзовидная')], default='spiral', max_length=20, verbose_name='Тип')),
                ('distance_ly', models.PositiveIntegerField(blank=True, null=True, verbose_name='Расстояние, световые годы')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Галактика',
                'verbose_name_plural': 'Галактики',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('spectral_class', models.CharField(blank=True, choices=[('O', 'O — очень горячая'), ('B', 'B — горячая'), ('A', 'A — белая'), ('F', 'F — жёлто-белая'), ('G', 'G — жёлтая'), ('K', 'K — оранжевая'), ('M', 'M — красная')], max_length=1, verbose_name='Спектральный класс')),
                ('temperature_k', models.PositiveIntegerField(blank=True, null=True, verbose_name='Температура, K')),
                ('galaxy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='cosmos.galaxy', verbose_name='Галактика')),
            ],
            options={
                'verbose_name': 'Звезда',
                'verbose_name_plural': 'Звёзды',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('radius_km', models.PositiveIntegerField(blank=True, null=True, verbose_name='Радиус, км')),
                ('has_life', models.BooleanField(default=False, verbose_name='Возможна жизнь')),
                ('discovery_year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Год открытия')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planets', to='cosmos.star', verbose_name='Звезда')),
            ],
            options={
                'verbose_name': 'Планета',
                'verbose_name_plural': 'Планеты',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='star',
            constraint=models.UniqueConstraint(fields=('galaxy', 'name'), name='uniq_star_in_galaxy'),
        ),
        migrations.AddConstraint(
            model_name='planet',
            constraint=models.UniqueConstraint(fields=('star', 'name'), name='uniq_planet_in_star'),
        ),
    ]
