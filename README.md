## Stripe Django Test Task

### Запуск локально
```bash
docker-compose up --build
```

### Admin
Ссылка на стандартную админ панель: ```http://localhost:8000/admin```. Данные для входа:
```
login: admin
password: admin
```

### Stripe
Используется Stripe Checkout Session.


### Endpoints
- ```buy/<int:id>/``` -> ```session.id```.
- ```item/<int:id>/``` -> вернет html для оплаты, который переведет на ```stripe``` форму.
- ```order/<int:id>/``` -> ```session.id```.
- ```buy/order/<int:id>/``` -> вернет html для оплаты, который переведет на ```stripe``` форму.


### Flow
- Заходим в админ панель ```http://localhost:8000/admin```;
- Создаем ```Discount``` и ```Tax``` - заполняем поля кроме id;
- Создаем ```Order```;
- Создаем ```Items```;
- Создаем ```OrderItems```;

Далее можно перейти на ```http://localhost:8000/order/1/```, чтобы убедиться в результате, жмем ```Pay Order```. Далее следует действовать аналогично.
