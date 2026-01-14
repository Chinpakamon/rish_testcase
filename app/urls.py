from django.urls import path
from .views import buy_item, buy_order, item_detail, order_detail

urlpatterns = [
    path("buy/<int:id>/", buy_item),
    path("item/<int:id>/", item_detail),
    path("order/<int:id>/", order_detail),
    path("buy/order/<int:id>/", buy_order),
]
