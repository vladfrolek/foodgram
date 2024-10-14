Фудграм» — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Запуск бэкенда локально
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/vladfrolek/foodgram
```
cd backend
```
Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:

```
python manage.py migrate
```

Загрузите тестовые данные:
```
python manage.py import_csv_data
```

Запустить проект:

```
python manage.py runserver
```  

## Запуск проекта в контейнере через Docker

Находясь в папке infra, выполните команду  
```
docker compose up  
``` 
При выполнении этой команды контейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.

[Cпецификация API](http://localhost/api/docs/)


Технологии примененые в проекте:
1. Python,
2. Django,
3. Django Rest Framework,
4. Docker,
5. NGINX,
6. PostgreSQL,


URL адрес развернутого проекта foodgramvf.zapto.org

Доступ в [админ-панель](http://foodgramvf.zapto.org/admin):

login: v@gmail.com  
pass: 11223344qqww  

Автор 
Влад Фролек  
