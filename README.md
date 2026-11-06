# Вселенная

Учебный каталог глубокого космоса на Django: галактики, звёзды и планеты с
фильтрами, сортировками, поиском, пагинацией и адаптивным интерфейсом.

## Паттерны

**MTV (Model — Template — View)**

- `cosmos/models.py` — модели `Galaxy`, `Star`, `Planet`;
- `cosmos/templates/cosmos/` — шаблоны страниц;
- `cosmos/views.py` — обработка запросов и сборка контекста.

**Repository**

- `cosmos/repositories.py` — весь доступ к базе данных;
- view-функции не пишут ORM-запросы, а вызывают методы репозиториев;
- агрегаты и статистика тоже вынесены в `StatisticsRepository`.

## Возможности

- главная страница с поиском, фильтром по типу галактики и сортировкой;
- карточки галактик с числом звёзд и планет, визуализацией типа;
- страница галактики: поиск и фильтр звёзд по спектральному классу,
  спектральная диаграмма;
- каталог планет: поиск по планете, звезде и галактике, фильтры по типу и
  наличию жизни, сортировка по радиусу, расстоянию и году открытия,
  пагинация и блок рекордов;
- страницы звезды и планеты с паспортом объекта и соседними объектами;
- админка с inline-редактированием и автодополнением;
- тёмная космическая тема, адаптивность, анимации появления.

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_universe
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/
Админка: http://127.0.0.1:8000/admin/

## Данные

Демонстрационный набор: 8 галактик, 10 звёзд и 21 планета.

```bash
python manage.py seed_universe           # добавить или обновить данные
python manage.py seed_universe --reset   # очистить и загрузить заново
```

## Структура

```text
SMI/
├── manage.py
├── requirements.txt
├── cosmos/
│   ├── models.py
│   ├── repositories.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   ├── templatetags/cosmos_extras.py
│   ├── management/commands/seed_universe.py
│   ├── migrations/
│   ├── static/cosmos/
│   └── templates/cosmos/
└── universe_project/
```

## Тесты

```bash
python manage.py test
```

16 тестов проверяют репозитории, фильтры, сортировки, статистику и страницы.
