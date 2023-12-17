# Purchase_Service
Сервис товаров для авторизованных пользователей.

### Stack:
- Python 3;
- FastAPI;
- PostgreSQL;
- Alembic;
- SQLAlchemy;
- JWT.

### Установка и запуск:
###### ВАЖНО! До начала выполнения комманд, создать файл .env и по примеру из проекта указать необходимые переменные.
- git clone https://github.com/Idvri/Purchase_Service.git;
- python -m venv venv (находясь в папке проекта);
- env/Scripts/activate (Windows);
- source venv/bin/activate (Linux);
- pip install -r requirements.txt;
- alembic upgrade head;
- cd src;
- uvicorn main:app --reload.
###### Можно так же с Poetry: poetry install --no-root, poetry shell.

### Доступность (адреса):
- 127.0.0.1:8000;
- localhost:8000.

### Функционал:
###### Документация API: http://localhost:8000/docs
- регистрация по email и номеру телефона;
- авторизация по email или номеру телефона;
- возможность просматривать доступные товары после авторизации;
- возможность просматривать содержимое своей корзины;
- добавление одного или нескольких товаров в корзину по названию;
- удаление товаров из корзины по названию;
- полная отчистка корзины.
