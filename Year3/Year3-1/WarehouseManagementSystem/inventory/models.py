from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


# =========================
# 物品表
# =========================
class Item(models.Model):

    name = models.CharField(max_length=100)

    category = models.CharField(max_length=100, blank=True)

    quantity = models.IntegerField(default=0)

    location = models.CharField(max_length=200, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("正常", "正常"),
            ("停用", "停用"),
        ],
        default="正常",
    )

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_items"
    )

    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="modified_items",
    )

    last_modified_time = models.DateTimeField(auto_now=True)
    current_location_image = models.ImageField(
        upload_to="current_location/", null=True, blank=True
    )

    purchase_date = models.DateField(null=True, blank=True, verbose_name="购买时间")

    valid_period = models.IntegerField(null=True, blank=True, verbose_name="有效期(月)")

    expiry_date = models.DateField(null=True, blank=True, verbose_name="失效时间")

    expiration_date = models.DateField(null=True, blank=True)

    @property
    def expiration_status(self):
        """
        判断物品有效期状态
        """

        # 没有失效日期
        if not self.expiry_date:
            return "未知"

        today = timezone.now().date()

        # 已过期
        if today > self.expiry_date:

            return "已过期"

        # 计算剩余天数
        remaining_days = (self.expiry_date - today).days

        # 30天内过期
        if remaining_days <= 30:

            return "即将过期"

        return "正常"

    def __str__(self):
        return self.name


# =========================
# 动态属性表
# =========================
class ItemAttribute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="attributes")

    key = models.CharField(max_length=50)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.item.name}-{self.key}"


# =========================
# 库存流水表
# =========================
class StockRecord(models.Model):

    TYPE_CHOICES = [
        ("IN", "增加库存"),
        ("OUT", "减少库存"),
    ]

    REASON_CHOICES = [
        ("INITIAL", "首次入库"),
        ("PURCHASE", "采购入库"),
        ("RETURN", "归还入库"),
        ("TRANSFER_IN", "调拨入库"),
        ("BORROW", "借出"),
        ("SCRAP", "报废"),
        ("DAMAGE", "损坏"),
        ("TRANSFER_OUT", "调拨"),
        ("CHECK", "盘点减少"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    reason = models.CharField(max_length=50, choices=REASON_CHOICES)

    quantity = models.IntegerField()

    remark = models.CharField(max_length=200, blank=True)

    location_image = models.ImageField(
        upload_to="location_records/", null=True, blank=True
    )

    created_time = models.DateTimeField(auto_now_add=True)


class ItemChangeLog(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    field = models.CharField(max_length=100)

    old_value = models.CharField(max_length=255, blank=True)

    new_value = models.CharField(max_length=255, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name}-{self.field}"
