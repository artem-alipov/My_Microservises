# My_Microservices Project

Этот проект состоит из нескольких микросервисов, включая `user-service`, `order-service` и `gateway-service`. Эти сервисы взаимодействуют друг с другом через gRPC и управляются с помощью Docker Compose.

## Запуск проекта

### Предварительные требования

- Docker
- Docker Compose

Запустите Docker Compose:

docker-compose up --build -d

Убедитесь, что все сервисы запущены корректно:

docker-compose ps

### Использование API

## User Service

Создание пользователя

curl -X POST http://localhost:7070/v1/user/create -H "Content-Type: application/json" -d '{  "id": 1,  "name": "User Name",  "email": "user.name@example.com",  "age": 30}'

Пример ответа:   "message": "User added successfully"

Если пользователь существует микросервис вернет собщение 'User with this ID already exists'

Ответ со сатутсом о выполнении запроса реализован для всех типов запросов реализванных в рамках данного проекта.

Получение информации о пользователе

curl -X GET http://localhost:7070/v1/user/1

Обновление информации о пользователе

curl -X PUT http://localhost:7070/v1/user/update -H "Content-Type: application/json" -d '{ "id": 1, "name": "New User Name", "email": "new.user.name@example.com", "age": 31}'

## Order Service

Создание заказа

curl -X POST http://localhost:7070/v1/order/create -H "Content-Type: application/json" -d '{ "id": 1, "title": "New Order", "description": "This is a new order", "user_id": 1}'

Получение информации о заказе

curl -X GET http://localhost:7070/v1/order/1

Обновление информации о заказе

curl -X PUT http://localhost:7070/v1/order/update -H "Content-Type: application/json" -d '{ "id": 1, "title": "Updated Order", "description": "This is an updated order", "user_id": 1}'

