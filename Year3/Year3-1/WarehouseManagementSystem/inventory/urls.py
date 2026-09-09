from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.inventory_list,
        name="inventory_list"
    ),


    path(
        "create/",
        views.create_item,
        name="create_item"
    ),

    path(
        "detail/<int:id>/",
        views.item_detail,
        name="item_detail"
    ),

    path(
        "stock_in/<int:id>/",
        views.stock_in,
        name="stock_in"
    ),


    path(
        "increase/<int:id>/",
        views.increase_stock,
        name="increase_stock"
    ),

]