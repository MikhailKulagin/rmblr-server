**rmblr-server**

Веб-сервис создан для отображегния данных по полкам (shelf) из БД coffepoint.  
Для просмотра всех полок используем. Чашки группируются по полкам 
с указанием объемов, владельцев и списка материалов. 

`http://127.0.0.1:8000/accounting` 

Для просмотра всех чашек юзера. Отоборажение всех чашек 
пользователя без привяки к полкам.  

`http://127.0.0.1:8000/accounting/users/%username%/`

Запуск сервиса:

`python3 manage.py runserver`

Запуск всех тестов:

`python3 manage.py test`

Проект:

```.
├── README.md
├── __init__.py
└── coffepoint
    ├── __init__.py
    ├── accounting
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── templates
    │   │   ├── _cup_table.html
    │   │   ├── base.html
    │   │   ├── index.html
    │   │   └── user.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── coffepoint
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── db.sqlite3
    └── manage.py
```

Добавление записи в таблицу:

`python3 manage.py shell`

`from accounting.models import Cup, Material, CupMaterials, Shelf, User`

`Cup(owner_id=1, shelf_id=1, volume=1, id=1).save()`

Файл БД db.sqlite3 включает в себя служебные таблицы SQLite и 
таблицы accounting_* с данными по кофепоинту. 
