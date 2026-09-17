from django import forms
from django.core.validators import FileExtensionValidator

from .models import Asset, StockRecord


MAX_IMAGE_SIZE = 5 * 1024 * 1024


def validate_image_size(image):
    if image.size > MAX_IMAGE_SIZE:
        raise forms.ValidationError("图片大小不能超过 5MB")


class InventoryImageForm(forms.Form):
    location_image = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp"]
            ),
            validate_image_size,
        ],
        error_messages={"invalid_image": "上传文件必须是有效的 JPG、PNG 或 WebP 图片"},
    )


class CreateItemForm(InventoryImageForm):
    name = forms.CharField(max_length=100, strip=True)
    category = forms.CharField(max_length=100, required=False, strip=True)
    quantity = forms.IntegerField(min_value=1)
    is_serialized = forms.TypedChoiceField(
        choices=[("0", "普通库存"), ("1", "单件设备管理")],
        coerce=lambda value: value == "1",
    )
    location = forms.CharField(max_length=200, required=False, strip=True)
    purchase_date = forms.DateField(required=False)
    valid_period = forms.IntegerField(required=False, min_value=1)
    expiry_date = forms.DateField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        is_serialized = cleaned_data.get("is_serialized")
        serial_numbers = [
            value.strip()
            for value in self.data.getlist("serial_numbers")
            if value.strip()
        ]

        if is_serialized and quantity:
            if len(serial_numbers) != quantity:
                self.add_error(None, f"单件设备必须填写 {quantity} 个设备编码")
            elif len(set(serial_numbers)) != len(serial_numbers):
                self.add_error(None, "设备编码不能重复")
            elif Asset.objects.filter(serial_number__in=serial_numbers).exists():
                self.add_error(None, "设备编码已存在")

        date_values = [
            cleaned_data.get("purchase_date"),
            cleaned_data.get("valid_period"),
            cleaned_data.get("expiry_date"),
        ]
        if sum(value is not None for value in date_values) < 2:
            self.add_error(None, "购买时间、有效期、失效时间至少填写两个")

        purchase_date = cleaned_data.get("purchase_date")
        expiry_date = cleaned_data.get("expiry_date")
        if purchase_date and expiry_date and expiry_date < purchase_date:
            self.add_error("expiry_date", "失效日期不能早于购买日期")

        cleaned_data["serial_numbers"] = serial_numbers
        return cleaned_data


class BaseStockForm(InventoryImageForm):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, item, **kwargs):
        self.item = item
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        serial_numbers = [
            value.strip()
            for value in self.data.getlist("serial_numbers")
            if value.strip()
        ]

        if self.item.is_serialized and quantity:
            if len(serial_numbers) != quantity:
                self.add_error(
                    None, f"单件设备必须填写 {quantity} 个设备编码"
                )
            elif len(set(serial_numbers)) != len(serial_numbers):
                self.add_error(None, "设备编码不能重复")

        cleaned_data["serial_numbers"] = serial_numbers
        return cleaned_data


class IncreaseStockForm(BaseStockForm):
    reason = forms.ChoiceField(
        choices=[
            ("PURCHASE", "采购入库"),
            ("RETURN", "归还入库"),
            ("TRANSFER_IN", "调拨入库"),
        ]
    )


class ExistingStockForm(BaseStockForm):
    pass


class DecreaseStockForm(BaseStockForm):
    reason = forms.ChoiceField(
        choices=[
            choice
            for choice in StockRecord.REASON_CHOICES
            if choice[0] in {"BORROW", "SCRAP", "DAMAGE", "TRANSFER_OUT", "CHECK"}
        ]
    )
    remark = forms.CharField(max_length=200, strip=True)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity > self.item.quantity:
            raise forms.ValidationError("减少数量不能超过当前库存")
        return quantity
