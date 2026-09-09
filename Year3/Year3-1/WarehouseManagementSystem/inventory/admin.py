from django.contrib import admin

from .models import (
    Item,
    ItemAttribute,
    StockRecord
)


class AttributeInline(admin.TabularInline):
    model = ItemAttribute
    extra = 1



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "quantity",
        "status",
        "created_by",
        "created_time"
    )
    inlines = [
        AttributeInline,
    ]



@admin.register(ItemAttribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "key",
        "value"
    )