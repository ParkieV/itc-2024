# 🏅 ИТ-чемпионат ИТС г. Москва. Разработка веб-приложения "Цифровая карта строительства (реконструкции) дорог и дорожных сооружений"

Проект решает проблему мониторинга строительства и реконструкции дорожных сооружений. На платформе
также предоставлена аналитика эффективности работы, прогнозирование задержек.

## Установка и запуск проекта
### Конфигурационный файл проекта
Ниже приведены необходимые настройки для запуска проекта. В проекте уже есть .env, но **настоятельно** рекомендуется поменять секретные ключи и другие настройки в целях безопасности.
```
#Database
DB_DRIVER="mongodb"
DB_USER_NAME = "adminzzzzs"
DB_PASSWORD = "secretz"
DB_HOST = mongo
DB_PORT =
DB_NAME = "local_db"

# Backend
BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 8000
BACKEND_ALLOW_ORIGINS = ["http://localhost","http://localhost:4200","http://localhost:9000","http://127.0.0.1:9000","https://localhost","https://localhost:4200","https://localhost:3000"]
BACKEND_ALLOW_CREDENTIALS = True
BACKEND_ALLOW_METHODS = ["GET","POST","DELETE","PATCH","OPTIONS"]
BACKEND_ALLOW_HEADERS = ["Access-Control-Allow-Origin","Authorization","User-Agent","Connection","Host","Content-Type","Accept","Accept-Encoding"]
BACKEND_PUBLIC_URL = "http://localhost:8000"

#Auth
AUTH_SECRET_KEY=
AUTH_ALGORITHM="HS256"
AUTH_ACCESS_TOKEN_EXPIRED_MINUTES=30
AUTH_REFRESH_TOKEN_EXPIRED_DAYS=30

```
### Инструкция к запуску
Необходимо в консоли перейти в корневой каталог проекта и запустить команду `docker compose up -d`

## Основной функционал проекта
— Интерактивная карта для отслеживания состояния дорожных объектов и работы подрядчиков.
— Возможность создания новых объектов и анализа дорожного полотна.
— Чат-бот, который помогает классифицировать дефекты по ГОСТу.
— Модель машинного обучения, предсказывающая поломки дорожных объектов.

## Технологии и инструменты

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Команда проекта
TODO: Дописать про себя что сделали

[Плужников Артем](https://github.com/TheTom205) - ML-engineer, разработка чат-бота

[Душенев Даниил](https://github.com/daniil-dushenev) - DS, декомпозиция задач

[Соловьев Вадим](https://github.com/vdmkkk) - Frontend, ...

[Рябцев Никита](https://github.com/nick-bkwp) - Frontend, Фронтенд, Дизайн, Аналитика

[Пискунов Степан](https://github.com/ParkieV) - Backend, разработка серверной части приложение, развертывание решения

[Горин Александр](https://github.com/AlexxxGorin) - ML-engineer, разработка модели детекции ям на дорогах

## Демонстрация работы прототипа
![изображение](https://github.com/user-attachments/assets/d6cc5f05-6cda-4b1a-a6c2-b8afe5e4298e)

## Заключение
Наш проект имеет удобный интерфейс мониторинга на карте работы над дорожными объектами. Имеет
аналитику работы инженеров, анализ дорожного полотна на наличие ям с помощью компьютерного зрения,
чат-бот для работы с базой знаний для консультации клиентов, прогнозирование выхода из строя объектов.
Все это помогает удобно и эффективно мониторить процесс строительства и реконструкции дорог.
