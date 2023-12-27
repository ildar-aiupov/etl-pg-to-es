# Микросервис непрерывного ETL-процесса миграции данных из PostgreSQL в ElasticSearch

### Описание
Микросервис выполняет непрерывный ETL-процесс миграции данных из базы PostgreSQL в хранилище ElasticSearch. Сервис с заданной периодичностью проверяет изменения данных в PostgreSQL, после чего актуализирует данные в хранилище ElasticSearch (в измененной части) и снова переходит в режим ослеживания изменений. Реализованы алгоритмы сохранения состояния сервиса и обеспечения его устойчивости к падениям PostgreSQL и ElasticSearch.  
Автор: Аюпов Ильдар, 2023 г., ildarbon@gmail.com  
Основные технологии и библиотеки:
- PostgreSQL
- ElasticSearch
- requests
- Docker

### Инструкция по запуску API
- клонировать настоящий репозиторий
- в корне проекта переименовать файл ```.env.example``` в ```.env``` (все настройки рабочие; ничего менять не нужно)
- в корне проекта выполнить команду ```docker compose up```. Отобразится процесс сборки контейнеров, после чего сервис заработает.
