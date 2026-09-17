from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory_list, name="inventory_list"),
    path("create/", views.create_item, name="create_item"),
    path("detail/<int:id>/", views.item_detail, name="item_detail"),
    path("stock_in/<int:id>/", views.increase_stock, name="stock_in"),
    path("increase/<int:id>/", views.increase_stock, name="increase_stock"),
    path("update/<int:id>/", views.update_item, name="update_item"),
    path("disable/<int:id>/", views.disable_item, name="disable_item"),
    path("enable/<int:id>/", views.enable_item, name="enable_item"),
    path("decrease/<int:id>/", views.decrease_stock, name="decrease_stock"),
    path("records/<int:id>/", views.stock_records, name="stock_records"),
    path("export/", views.export_csv, name="export_csv"),
    path("export/all/", views.export_inventory_all, name="export_inventory_all"),
    path("user-records/", views.user_records, name="user_records"),
    path(
        "export/filter/", views.export_inventory_filter, name="export_inventory_filter"
    ),
    path("photo/<int:id>/", views.record_photo, name="record_photo"),
    path("item/<int:item_id>/assets/", views.asset_list, name="asset_list"),
]
