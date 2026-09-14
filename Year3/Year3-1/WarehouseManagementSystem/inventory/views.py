from accounts.models import UserProfile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, ItemAttribute, StockRecord
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime


def admin_required(request):

    if not request.user.is_authenticated:

        return False

    if request.user.userprofile.role != "ADMIN":

        return False

    return True


from django.db.models import Sum
from django.contrib.auth.models import User

@login_required
def index(request):

    user = request.user

    if user.is_authenticated and user.userprofile.role == "ADMIN":

        pending_count = UserProfile.objects.filter(status="PENDING").count()
        user_count = User.objects.count()

        disabled_count = UserProfile.objects.filter(status="DISABLED").count()
        item_count = Item.objects.count()

        total_quantity = Item.objects.aggregate(Sum("quantity"))["quantity__sum"] or 0

        recent_records = StockRecord.objects.order_by("-created_time")[:10]

        return render(
            request,
            "inventory/admin_index.html",
            {
                "pending_count": pending_count,
                "user_count": user_count,
                "disabled_count": disabled_count,
                "item_count": item_count,
                "total_quantity": total_quantity,
                "recent_records": recent_records,
            },
        )

    else:

        return redirect("inventory_list")


from django.db.models import Q


def inventory_list(request):
    items = get_filtered_items(request)

    # =====================
    # 获取所有类别
    # =====================

    categories = (
        Item.objects.exclude(category="").values_list("category", flat=True).distinct()
    )
    username = request.GET.get("username", "").strip()

    if username:

        items = items.filter(created_by__username__icontains=username)

    # =====================
    # 搜索
    # =====================

    keyword = request.GET.get("keyword", "")

    # if keyword:

    #     items = items.filter(
    #         Q(name__icontains=keyword)
    #         | Q(category__icontains=keyword)
    #         | Q(location__icontains=keyword)
    #     )

    # # =====================
    # # 类别筛选
    # # =====================

    category = request.GET.get("category", "")

    if category:

        items = items.filter(category=category)

    # =====================
    # 状态筛选
    # =====================

    status = request.GET.get("status", "")

    if status:

        items = items.filter(status=status)

    return render(
        request,
        "inventory/inventory_list.html",
        {
            "username": username,
            "items": items,
            "keyword": keyword,
            "category": category,
            "status": status,
            "categories": categories,
        },
    )


@login_required
def create_item(request):

    # 权限检查
    if not admin_required(request):

        return HttpResponse("没有权限!")

    if request.method == "POST":

        # =====================
        # 判断是否增加已有物品
        # =====================

        add_existing = request.POST.get("add_existing")

        if add_existing:

            item_id = request.POST.get("item_id")

            item = get_object_or_404(Item, id=item_id)

            quantity_str = request.POST.get("quantity", "")

            if not quantity_str.isdigit() or int(quantity_str) <= 0:

                messages.error(request, "请输入正确的增加数量")

                return render(
                    request,
                    "inventory/create_item.html",
                    {
                        "name": request.POST.get("name"),
                        "category": request.POST.get("category"),
                        "quantity": quantity_str,
                        "location": request.POST.get("location"),
                    },
                )

            quantity = int(quantity_str)

            item.quantity += quantity

            image = request.FILES.get("location_image")

            if image:
                item.current_location_image = image

            item.save()

            StockRecord.objects.create(
                user=request.user,
                item=item,
                type="IN",
                quantity=quantity,
                reason="PURCHASE",
                location_image=request.FILES.get("location_image"),
            )

            messages.success(
                request,
                f"成功增加库存：{item.name} +{quantity}，当前库存 {item.quantity}",
            )

            return redirect("inventory_list")

        # =====================
        # 创建新物品
        # =====================

        name = request.POST.get("name", "").strip()

        category = request.POST.get("category", "")

        quantity_str = request.POST.get("quantity", "")

        location = request.POST.get("location", "")

        if not name:

            messages.error(request, "物品名称不能为空")

            return render(
                request,
                "inventory/create_item.html",
                {
                    "name": name,
                    "category": category,
                    "quantity": quantity_str,
                    "location": location,
                    "item_names": Item.objects.values_list(
                        "name", flat=True
                    ).distinct(),
                    "categories": Item.objects.values_list(
                        "category", flat=True
                    ).distinct(),
                },
            )

        if not quantity_str.isdigit() or int(quantity_str) <= 0:

            messages.error(request, "请输入正确的库存数量")

            # return render(request, "inventory/create_item.html")
            return render(
                request,
                "inventory/create_item.html",
                {
                    "name": name,
                    "category": category,
                    "quantity": quantity_str,
                    "location": location,
                    "item_names": Item.objects.values_list(
                        "name", flat=True
                    ).distinct(),
                    "categories": Item.objects.values_list(
                        "category", flat=True
                    ).distinct(),
                },
            )

        quantity = int(quantity_str)

        purchase_date_str = request.POST.get("purchase_date")

        valid_period_str = request.POST.get("valid_period")

        expiry_date_str = request.POST.get("expiry_date")

        purchase_date = None
        valid_period = None
        expiry_date = None

        try:

            if purchase_date_str:

                purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()

            if valid_period_str:

                if not valid_period_str.isdigit():

                    messages.error(request, "有效期必须是正整数")

                    return render(
                        request,
                        "inventory/create_item.html",
                        {
                            "name": name,
                            "category": category,
                            "quantity": quantity_str,
                            "location": location,
                            "purchase_date": purchase_date_str,
                            "valid_period": valid_period_str,
                            "expiry_date": expiry_date_str,
                        },
                    )

                valid_period = int(valid_period_str)

            if expiry_date_str:

                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()

        except ValueError:

            messages.error(request, "日期格式错误")

            return render(
                request,
                "inventory/create_item.html",
                {
                    "name": name,
                    "category": category,
                    "quantity": quantity_str,
                    "location": location,
                    "purchase_date": purchase_date_str,
                    "valid_period": valid_period_str,
                    "expiry_date": expiry_date_str,
                },
            )

        input_count = sum(
            [
                purchase_date is not None,
                valid_period is not None,
                expiry_date is not None,
            ]
        )

        if input_count < 2:

            messages.error(request, "购买时间、有效期、失效时间至少填写两个")

            return render(
                request,
                "inventory/create_item.html",
                {
                    "name": name,
                    "category": category,
                    "quantity": quantity_str,
                    "location": location,
                    "purchase_date": purchase_date_str,
                    "valid_period": valid_period_str,
                    "expiry_date": expiry_date_str,
                    "item_names": Item.objects.values_list(
                        "name", flat=True
                    ).distinct(),
                    "categories": Item.objects.values_list(
                        "category", flat=True
                    ).distinct(),
                },
            )

        # if purchase_date and valid_period and not expiry_date:

        #     expiry_date = purchase_date + relativedelta(months=valid_period)
        # if purchase_date and expiry_date and not valid_period:

        #     diff = relativedelta(expiry_date, purchase_date)

        #     valid_period = diff.years * 12 + diff.months

        # if valid_period and expiry_date and not purchase_date:

        #     purchase_date = expiry_date - relativedelta(months=valid_period)
        purchase_date, valid_period, expiry_date = calculate_expiry(
            purchase_date, valid_period, expiry_date
        )

        if purchase_date and expiry_date:

            if expiry_date < purchase_date:

                messages.error(request, "失效日期不能早于购买日期")

                return render(
                    request,
                    "inventory/create_item.html",
                    {
                        "name": name,
                        "category": category,
                        "quantity": quantity_str,
                        "location": location,
                        "purchase_date": purchase_date_str,
                        "valid_period": valid_period_str,
                        "expiry_date": expiry_date_str,
                        "item_names": Item.objects.values_list(
                            "name", flat=True
                        ).distinct(),
                        "categories": Item.objects.values_list(
                            "category", flat=True
                        ).distinct(),
                    },
                )

        image = request.FILES.get("location_image")

        # =====================
        # 检查重复物品
        # =====================

        same_item = Item.objects.filter(name=name, category=category).first()

        force_create = request.POST.get("force_create")

        if same_item and not force_create:
            messages.warning(
                request,
                f"发现已有相同物品：{same_item.name}，当前库存 {same_item.quantity}",
            )

            return render(
                request,
                "inventory/create_item.html",
                {
                    "warning": True,
                    "same_item": same_item,
                    "name": name,
                    "category": category,
                    "quantity": quantity_str,
                    "location": location,
                    "item_names": Item.objects.values_list(
                        "name", flat=True
                    ).distinct(),
                    "categories": Item.objects.values_list(
                        "category", flat=True
                    ).distinct(),
                    "purchase_date": purchase_date_str,
                    "valid_period": valid_period_str,
                    "expiry_date": expiry_date_str,
                    # 保留动态属性
                    "attribute_keys": request.POST.getlist("attribute_key"),
                    "attribute_values": request.POST.getlist("attribute_value"),
                },
            )

        # =====================
        # 创建新物品
        # =====================

        item = Item.objects.create(
            name=name,
            category=category,
            quantity=quantity,
            location=location,
            created_by=request.user,
            purchase_date=purchase_date,
            valid_period=valid_period,
            expiry_date=expiry_date,
            current_location_image=image,
            last_modified_by=request.user,
        )

        # =====================
        # 保存动态属性
        # =====================

        keys = request.POST.getlist("attribute_key")

        values = request.POST.getlist("attribute_value")

        for key, value in zip(keys, values):

            if key and value:

                ItemAttribute.objects.create(item=item, key=key, value=value)

        # =====================
        # 首次入库记录
        # =====================

        StockRecord.objects.create(
            user=request.user,
            item=item,
            type="IN",
            quantity=quantity,
            reason="INITIAL",
            location_image=image,
        )

        messages.success(request, f"物品 {item.name} 创建成功，库存 {quantity}")

        return redirect("inventory_list")

    return render(
        request,
        "inventory/create_item.html",
        {
            "item_names": Item.objects.values_list("name", flat=True).distinct(),
            "categories": Item.objects.values_list("category", flat=True).distinct(),
        },
    )


def validate_date(purchase_date, expiry_date):

    if purchase_date and expiry_date:

        if expiry_date < purchase_date:

            return False

    return True


def calculate_expiry(purchase_date, valid_period, expiry_date):

    # 1. 有购买日期 + 有效期，没有失效日期
    if purchase_date and valid_period and not expiry_date:

        expiry_date = purchase_date + relativedelta(months=valid_period)

    # 2. 有购买日期 + 失效日期，没有有效期
    if purchase_date and expiry_date and not valid_period:

        diff = relativedelta(expiry_date, purchase_date)

        valid_period = diff.years * 12 + diff.months

    # 3. 有效期 + 失效日期，没有购买日期
    if valid_period and expiry_date and not purchase_date:

        purchase_date = expiry_date - relativedelta(months=valid_period)

    # 4. 三个都有，但是数据不一致
    if purchase_date and valid_period and expiry_date:

        calculated_expiry = purchase_date + relativedelta(months=valid_period)

        # 如果计算出的失效日期和输入的不一致
        if calculated_expiry != expiry_date:

            diff = relativedelta(expiry_date, purchase_date)

            valid_period = diff.years * 12 + diff.months

    return purchase_date, valid_period, expiry_date


def record_photo(request, id):

    record = get_object_or_404(StockRecord, id=id)

    return render(request, "inventory/record_photo.html", {"record": record})


# def item_detail(request, id):
#     item = get_object_or_404(Item, id=id)

#     latest_record = (
#         StockRecord.objects.filter(item=item, location_image__isnull=False)
#         .order_by("-created_time")
#         .first()
#     )

#     return render(
#         request,
#         "inventory/item_detail.html",
#         {"item": item, "latest_record": latest_record},
#     )


@login_required
def item_detail(request, id):

    item = get_object_or_404(Item, id=id)

    records = StockRecord.objects.filter(item=item).order_by("-created_time")

    return render(
        request,
        "inventory/item_detail.html",
        {
            "item": item,
            # 最近操作记录
            "records": records,
            # "records": records[:10],
        },
    )


@login_required
def stock_in(request, id):

    # 权限检查

    if not admin_required(request):

        return HttpResponse("没有权限")

    item = get_object_or_404(Item, id=id)

    if request.method == "POST":

        quantity = int(request.POST["quantity"])

        if quantity <= 0:

            messages.error(request, "数量必须大于0")

            return redirect("stock_in", id=item.id)

        reason = request.POST.get("reason", "")

        image = request.FILES.get("location_image")
        if image:
            item.current_location_image = image

        # 修改库存数量

        item.quantity += quantity

        item.save()

        # 创建流水

        StockRecord.objects.create(
            user=request.user,
            item=item,
            type="IN",
            quantity=quantity,
            reason=reason,
            location_image=image,
        )

        return redirect("item_detail", id=item.id)

    return render(request, "inventory/stock_in.html", {"item": item})


from django.db import transaction


@login_required
def increase_stock(request, id):

    # 权限
    if not admin_required(request):

        return HttpResponse("没有权限")

    if request.method == "POST":

        # =====================
        # 数量检查
        # =====================

        try:

            quantity = int(request.POST.get("quantity", 0))

        except ValueError:

            messages.error(request, "请输入正确的增加数量")

            return redirect("increase_stock", id=id)

        with transaction.atomic():

            # =====================
            # 加锁，防止多人同时修改库存
            # =====================

            item = get_object_or_404(Item.objects.select_for_update(), id=id)

            if quantity <= 0:

                messages.error(request, "增加数量必须大于0")

                return redirect("increase_stock", id=item.id)

            # =====================
            # 获取入库信息
            # =====================

            reason = request.POST.get("reason", "")

            image = request.FILES.get("location_image")

            if image:

                item.current_location_image = image

            # =====================
            # 修改库存
            # =====================

            item.quantity += quantity
            item.last_modified_by = request.user
            item.save()

            # =====================
            # 创建库存流水
            # =====================

            StockRecord.objects.create(
                user=request.user,
                item=item,
                type="IN",
                quantity=quantity,
                reason=reason,
                location_image=image,
            )

        return redirect("item_detail", id=item.id)

    # =====================
    # GET 请求：显示页面
    # =====================

    item = get_object_or_404(Item, id=id)

    return render(request, "inventory/increase_stock.html", {"item": item})


from django.contrib import messages


@login_required
def decrease_stock(request, id):

    # 权限检查
    if not admin_required(request):

        return HttpResponse("没有权限!")

    if request.method == "POST":

        try:
            quantity = int(request.POST["quantity"])

        except ValueError:

            messages.error(request, "请输入正确数量")

            return redirect("decrease_stock", id=id)

        if quantity <= 0:

            messages.error(request, "数量必须大于0")

            return redirect("decrease_stock", id=id)

        reason = request.POST.get("reason", "")

        image = request.FILES.get("location_image")

        with transaction.atomic():

            item = Item.objects.select_for_update().get(id=id)

            # 防止库存不足

            if quantity > item.quantity:

                messages.error(request, "减少数量不能超过当前库存")

                return redirect("decrease_stock", id=item.id)

            item.quantity -= quantity

            if image:

                item.current_location_image = image
            item.last_modified_by = request.user
            item.save()

            StockRecord.objects.create(
                user=request.user,
                item=item,
                type="OUT",
                quantity=quantity,
                reason=reason,
                location_image=image,
            )

        messages.success(request, "库存减少成功")

        return redirect("item_detail", id=item.id)

    else:

        item = Item.objects.get(id=id)

    return render(request, "inventory/decrease_stock.html", {"item": item})


from .models import ItemChangeLog


def update_item(request, id):

    if not admin_required(request):
        return HttpResponse("没有权限")

    item = Item.objects.get(id=id)

    if request.method == "POST":
        # =====================
        # 保存修改前的数据
        # =====================

        old_values = {
            "name": item.name,
            "category": item.category,
            "location": item.location,
            "purchase_date": item.purchase_date,
            "valid_period": item.valid_period,
            "expiry_date": item.expiry_date,
        }

        item.name = request.POST["name"]

        item.category = request.POST.get("category", "")

        item.location = request.POST.get("location", "")

        purchase_date = None
        valid_period = None
        expiry_date = None

        purchase_date_str = request.POST.get("purchase_date")

        valid_period_str = request.POST.get("valid_period")

        expiry_date_str = request.POST.get("expiry_date")

        if purchase_date_str:

            purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()

        if valid_period_str:

            valid_period = int(valid_period_str)

        if expiry_date_str:

            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()

        # 调用统一计算逻辑
        purchase_date, valid_period, expiry_date = calculate_expiry(
            purchase_date, valid_period, expiry_date
        )

        item.purchase_date = purchase_date

        item.valid_period = valid_period

        item.expiry_date = expiry_date
        item.last_modified_by = request.user

        item.save()

        # =====================
        # 创建修改记录
        # =====================

        new_values = {
            "name": item.name,
            "category": item.category,
            "location": item.location,
            "purchase_date": item.purchase_date,
            "valid_period": item.valid_period,
            "expiry_date": item.expiry_date,
        }
        for field in old_values:

            if old_values[field] != new_values[field]:

                ItemChangeLog.objects.create(
                    item=item,
                    user=request.user,
                    field=field,
                    old_value=str(old_values[field]),
                    new_value=str(new_values[field]),
                )

        return redirect("item_detail", id=item.id)

    return render(request, "inventory/update_item.html", {"item": item})


def enable_item(request, id):

    if not admin_required(request):

        return HttpResponse("没有权限")

    item = get_object_or_404(Item, id=id)

    item.status = "正常"
    item.last_modified_by = request.user
    item.save()

    return redirect("inventory_list")


def disable_item(request, id):

    if not admin_required(request):

        return HttpResponse("没有权限")

    if request.method != "POST":

        return HttpResponse("非法请求")

    item = Item.objects.get(id=id)

    item.status = "停用"
    item.last_modified_by = request.user
    item.save()

    return redirect("inventory_list")


@login_required
def user_records(request):

    records = StockRecord.objects.all().order_by("-created_time")

    username = request.GET.get("username", "").strip()

    if username:

        records = records.filter(user__username__icontains=username)

    operation_type = request.GET.get("type", "")

    if operation_type:

        records = records.filter(type=operation_type)

    item_name = request.GET.get("item", "")

    if item_name:

        records = records.filter(item__name__icontains=item_name)

    users = User.objects.all()

    return render(
        request,
        "inventory/user_records.html",
        {
            "records": records,
            "users": users,
            "username": username,
            "operation_type": operation_type,
            "item_name": item_name,
        },
    )


def stock_records(request, id):
    item = get_object_or_404(Item, id=id)

    records = StockRecord.objects.filter(item=item).order_by("-created_time")

    return render(
        request, "inventory/stock_records.html", {"item": item, "records": records}
    )


def get_filtered_items(request):

    items = Item.objects.all()

    keyword = request.GET.get("keyword", "")

    if keyword:

        items = items.filter(
            Q(name__icontains=keyword)
            | Q(category__icontains=keyword)
            | Q(location__icontains=keyword)
        )

    # 创建者搜索
    username = request.GET.get("username", "").strip()

    if username:

        items = items.filter(created_by__username__icontains=username)

    category = request.GET.get("category", "")

    if category:

        items = items.filter(category=category)

    status = request.GET.get("status", "")

    if status:

        items = items.filter(status=status)

    return items


def export_inventory_all(request):

    items = Item.objects.all()

    return export_csv(items)


def export_inventory_filter(request):

    items = get_filtered_items(request)

    return export_csv(items)


import csv
from datetime import datetime


def export_csv(items):

    response = HttpResponse(content_type="text/csv")

    filename = "inventory_" + datetime.now().strftime("%Y_%m_%d") + ".csv"

    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    writer.writerow(["编号", "名称", "类别", "数量", "位置", "状态", "创建时间"])

    for item in items:

        writer.writerow(
            [
                item.id,
                item.name,
                item.category,
                item.quantity,
                item.location,
                item.status,
                item.created_time,
            ]
        )

    return response
