from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile
from .models import Asset, Item, StockRecord


class SerializedInventoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="password")
        UserProfile.objects.create(
            user=self.user,
            real_name="管理员",
            role="ADMIN",
            status="APPROVED",
        )
        self.client.force_login(self.user)

    def create_item(self, name, is_serialized=False, serial_numbers=None):
        return self.client.post(
            reverse("create_item"),
            {
                "name": name,
                "category": "电机",
                "quantity": str(len(serial_numbers) if serial_numbers else 1),
                "is_serialized": "1" if is_serialized else "0",
                "serial_numbers": serial_numbers or [],
                "purchase_date": "2026-01-01",
                "valid_period": "12",
            },
        )

    def test_normal_inventory_still_blocks_duplicate_item(self):
        self.assertRedirects(self.create_item("普通电机"), reverse("inventory_list"))

        duplicate_response = self.create_item("普通电机")

        self.assertEqual(duplicate_response.status_code, 200)
        self.assertContains(duplicate_response, "发现已有相同物品")
        self.assertNotContains(duplicate_response, "仍然创建新物品")
        self.assertEqual(Item.objects.filter(name="普通电机").count(), 1)

    def test_serialized_item_requires_one_unique_code_per_unit(self):
        missing_code_response = self.create_item(
            "m3508电机", is_serialized=True, serial_numbers=[]
        )
        self.assertContains(missing_code_response, "单件设备必须填写 1 个编码")
        self.assertFalse(Item.objects.exists())

        response = self.create_item(
            "m3508电机", is_serialized=True, serial_numbers=["x12345", "x120000"]
        )
        self.assertRedirects(response, reverse("inventory_list"))
        item = Item.objects.get(name="m3508电机")
        self.assertEqual(item.quantity, 2)
        self.assertCountEqual(
            item.assets.values_list("serial_number", flat=True),
            ["x12345", "x120000"],
        )

    def test_same_serialized_name_groups_new_codes_under_existing_item(self):
        self.assertRedirects(
            self.create_item("同型号电机", True, ["GROUP-001"]),
            reverse("inventory_list"),
        )
        existing = Item.objects.get(name="同型号电机")

        warning_response = self.create_item("同型号电机", True, ["GROUP-002"])
        self.assertContains(warning_response, "将设备编码加入已有物品")

        response = self.client.post(
            reverse("create_item"),
            {
                "add_existing": "1",
                "item_id": str(existing.id),
                "name": existing.name,
                "quantity": "1",
                "is_serialized": "1",
                "serial_numbers": ["GROUP-002"],
            },
        )

        self.assertRedirects(response, reverse("inventory_list"))
        existing.refresh_from_db()
        self.assertEqual(Item.objects.filter(name="同型号电机").count(), 1)
        self.assertEqual(existing.quantity, 2)
        self.assertCountEqual(
            existing.assets.values_list("serial_number", flat=True),
            ["GROUP-001", "GROUP-002"],
        )

    def test_category_is_optional(self):
        response = self.client.post(
            reverse("create_item"),
            {
                "name": "无类别物品",
                "category": "",
                "quantity": "1",
                "is_serialized": "0",
                "purchase_date": "2026-01-01",
                "valid_period": "12",
            },
        )

        self.assertRedirects(response, reverse("inventory_list"))
        self.assertEqual(Item.objects.get(name="无类别物品").category, "")

    def test_invalid_form_keeps_serials_and_other_values(self):
        response = self.client.post(
            reverse("create_item"),
            {
                "name": "待修正设备",
                "category": "测试类别",
                "quantity": "2",
                "location": "A-01",
                "is_serialized": "1",
                "serial_numbers": ["KEEP-001", ""],
                "purchase_date": "2026-01-01",
                "valid_period": "12",
                "attribute_key": ["品牌"],
                "attribute_value": ["测试品牌"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "单件设备必须填写 2 个编码")
        self.assertContains(response, "KEEP-001")
        self.assertContains(response, "A-01")
        self.assertContains(response, "测试品牌")

        html = response.content.decode()
        data_script_position = html.index('id="initial-serial-numbers"')
        main_script_position = html.index("<script>", data_script_position)
        self.assertLess(data_script_position, main_script_position)

    def test_item_detail_lists_all_device_codes(self):
        item = Item.objects.create(
            name="多编码设备", is_serialized=True, quantity=2, created_by=self.user
        )
        Asset.objects.create(item=item, serial_number="DETAIL-001")
        Asset.objects.create(item=item, serial_number="DETAIL-002")

        response = self.client.get(reverse("item_detail", args=[item.id]))

        self.assertContains(response, "单件设备明细")
        self.assertContains(response, "DETAIL-001")
        self.assertContains(response, "DETAIL-002")

    def test_serialized_stock_in_requires_codes(self):
        item = Item.objects.create(
            name="单件电机", is_serialized=True, quantity=1, created_by=self.user
        )
        Asset.objects.create(item=item, serial_number="SN-1")
        url = reverse("increase_stock", args=[item.id])

        response = self.client.post(url, {"quantity": "1", "reason": "PURCHASE"})
        self.assertRedirects(response, url)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)

        self.client.post(
            url,
            {"quantity": "1", "reason": "PURCHASE", "serial_numbers": ["SN-2"]},
        )
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)
        self.assertTrue(item.assets.filter(serial_number="SN-2").exists())

    def test_serialized_stock_out_requires_available_matching_codes(self):
        item = Item.objects.create(
            name="单件电机", is_serialized=True, quantity=2, created_by=self.user
        )
        first = Asset.objects.create(item=item, serial_number="SN-1")
        Asset.objects.create(item=item, serial_number="SN-2")
        url = reverse("decrease_stock", args=[item.id])

        response = self.client.post(
            url,
            {
                "quantity": "1",
                "reason": "BORROW",
                "remark": "测试用途",
                "serial_numbers": ["WRONG"],
            },
        )
        self.assertRedirects(response, url)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(StockRecord.objects.count(), 0)

        self.client.post(
            url,
            {
                "quantity": "1",
                "reason": "BORROW",
                "remark": "用于一号生产线",
                "serial_numbers": ["SN-1"],
            },
        )
        item.refresh_from_db()
        first.refresh_from_db()
        self.assertEqual(item.quantity, 1)
        self.assertEqual(first.status, "BORROWED")
        record = StockRecord.objects.get()
        self.assertEqual(record.asset, first)
        self.assertEqual(record.remark, "用于一号生产线")

    def test_stock_out_form_and_backend_limit_quantity_to_current_stock(self):
        item = Item.objects.create(
            name="限量设备", is_serialized=True, quantity=2, created_by=self.user
        )
        Asset.objects.create(item=item, serial_number="LIMIT-001")
        Asset.objects.create(item=item, serial_number="LIMIT-002")
        url = reverse("decrease_stock", args=[item.id])

        get_response = self.client.get(url)
        self.assertContains(get_response, 'max="2"')

        post_response = self.client.post(
            url,
            {
                "quantity": "3",
                "reason": "BORROW",
                "remark": "超量测试",
                "serial_numbers": ["LIMIT-001", "LIMIT-002", "LIMIT-003"],
            },
        )
        self.assertRedirects(post_response, url)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(StockRecord.objects.count(), 0)

    def test_normal_stock_out_does_not_require_device_code(self):
        item = Item.objects.create(
            name="普通电机", is_serialized=False, quantity=2, created_by=self.user
        )

        self.client.post(
            reverse("decrease_stock", args=[item.id]),
            {"quantity": "1", "reason": "SCRAP", "remark": "报废处理"},
        )

        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)

    def test_stock_out_requires_purpose(self):
        item = Item.objects.create(
            name="用途测试", is_serialized=False, quantity=2, created_by=self.user
        )
        url = reverse("decrease_stock", args=[item.id])

        response = self.client.post(url, {"quantity": "1", "reason": "SCRAP"})

        self.assertRedirects(response, url)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)
        self.assertFalse(StockRecord.objects.exists())

    def test_inventory_search_supports_device_code_and_combined_filters(self):
        matching = Item.objects.create(
            name="编码搜索设备",
            category="电机",
            status="正常",
            is_serialized=True,
            quantity=1,
            created_by=self.user,
        )
        Asset.objects.create(item=matching, serial_number="SEARCH-X12345")
        other = Item.objects.create(
            name="其他设备",
            category="工具",
            status="正常",
            is_serialized=True,
            quantity=1,
            created_by=self.user,
        )
        Asset.objects.create(item=other, serial_number="OTHER-001")

        code_response = self.client.get(
            reverse("inventory_list"), {"serial_number": "X12345"}
        )
        self.assertContains(code_response, matching.name)
        self.assertNotContains(code_response, other.name)

        keyword_response = self.client.get(
            reverse("inventory_list"),
            {"keyword": "SEARCH-X", "category": "电机", "status": "正常"},
        )
        self.assertContains(keyword_response, matching.name)
        self.assertNotContains(keyword_response, other.name)
