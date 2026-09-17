from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Asset, Item, ItemAttribute, StockRecord


@transaction.atomic
def create_inventory_item(
    *,
    user,
    name,
    category,
    quantity,
    is_serialized,
    location,
    purchase_date,
    valid_period,
    expiry_date,
    serial_numbers,
    attributes,
    image=None,
):
    item = Item.objects.create(
        name=name,
        category=category,
        quantity=quantity,
        is_serialized=is_serialized,
        location=location,
        created_by=user,
        purchase_date=purchase_date,
        valid_period=valid_period,
        expiry_date=expiry_date,
        current_location_image=image,
        last_modified_by=user,
    )

    for key, value in attributes:
        if key and value:
            ItemAttribute.objects.create(item=item, key=key, value=value)

    created_assets = []
    if is_serialized:
        created_assets = [
            Asset.objects.create(item=item, serial_number=serial)
            for serial in serial_numbers
        ]

    if is_serialized:
        for index, asset in enumerate(created_assets):
            StockRecord.objects.create(
                user=user,
                item=item,
                asset=asset,
                type="IN",
                quantity=1,
                reason="INITIAL",
                location_image=image if index == 0 else None,
            )
    else:
        StockRecord.objects.create(
            user=user,
            item=item,
            type="IN",
            quantity=quantity,
            reason="INITIAL",
            location_image=image,
        )

    return item


@transaction.atomic
def add_existing_item_stock(
    *, item_id, user, quantity, serial_numbers, image=None
):
    item = Item.objects.select_for_update().get(id=item_id)
    added_assets = []

    if item.is_serialized:
        if Asset.objects.filter(serial_number__in=serial_numbers).exists():
            raise ValidationError("设备编码已存在")
        added_assets = [
            Asset.objects.create(item=item, serial_number=serial)
            for serial in serial_numbers
        ]

    item.quantity += quantity
    item.last_modified_by = user
    if image:
        item.current_location_image = image
    item.save()

    if item.is_serialized:
        for index, asset in enumerate(added_assets):
            StockRecord.objects.create(
                user=user,
                item=item,
                asset=asset,
                type="IN",
                quantity=1,
                reason="PURCHASE",
                location_image=image if index == 0 else None,
            )
    else:
        StockRecord.objects.create(
            user=user,
            item=item,
            type="IN",
            quantity=quantity,
            reason="PURCHASE",
            location_image=image,
        )

    return item


@transaction.atomic
def increase_item_stock(*, item_id, user, quantity, reason, serial_numbers, image=None):
    item = Item.objects.select_for_update().get(id=item_id)
    stocked_assets = []

    if item.is_serialized:
        existing_assets = {
            asset.serial_number: asset
            for asset in Asset.objects.select_for_update().filter(
                serial_number__in=serial_numbers
            )
        }

        for serial in serial_numbers:
            existing_asset = existing_assets.get(serial)
            can_return = (
                reason == "RETURN"
                and existing_asset
                and existing_asset.item_id == item.id
                and existing_asset.status == "BORROWED"
            )
            if existing_asset and not can_return:
                raise ValidationError(f"设备编码 {serial} 已存在或不可入库")

        for serial in serial_numbers:
            asset = existing_assets.get(serial)
            if asset:
                asset.status = "AVAILABLE"
                asset.save(update_fields=["status"])
            else:
                asset = Asset.objects.create(item=item, serial_number=serial)
            stocked_assets.append(asset)

    item.quantity += quantity
    item.last_modified_by = user
    if image:
        item.current_location_image = image
    item.save()

    if item.is_serialized:
        for index, asset in enumerate(stocked_assets):
            StockRecord.objects.create(
                user=user,
                item=item,
                asset=asset,
                type="IN",
                quantity=1,
                reason=reason,
                location_image=image if index == 0 else None,
            )
    else:
        StockRecord.objects.create(
            user=user,
            item=item,
            type="IN",
            quantity=quantity,
            reason=reason,
            location_image=image,
        )

    return item


@transaction.atomic
def decrease_item_stock(
    *, item_id, user, quantity, reason, remark, serial_numbers, image=None
):
    item = Item.objects.select_for_update().get(id=item_id)
    if quantity > item.quantity:
        raise ValidationError("减少数量不能超过当前库存")

    selected_assets = []
    if item.is_serialized:
        selected_assets = list(
            Asset.objects.select_for_update().filter(
                item=item,
                serial_number__in=serial_numbers,
                status="AVAILABLE",
            )
        )
        if len(selected_assets) != quantity:
            raise ValidationError("存在不属于当前物品或当前不可用的设备编码")

    item.quantity -= quantity
    item.last_modified_by = user
    if image:
        item.current_location_image = image
    item.save()

    if item.is_serialized:
        new_status = {"BORROW": "BORROWED", "DAMAGE": "DAMAGED"}.get(
            reason, "OUT"
        )
        for index, asset in enumerate(selected_assets):
            asset.status = new_status
            asset.save(update_fields=["status"])
            StockRecord.objects.create(
                user=user,
                item=item,
                asset=asset,
                type="OUT",
                quantity=1,
                reason=reason,
                remark=remark,
                location_image=image if index == 0 else None,
            )
    else:
        StockRecord.objects.create(
            user=user,
            item=item,
            type="OUT",
            quantity=quantity,
            reason=reason,
            remark=remark,
            location_image=image,
        )

    return item
