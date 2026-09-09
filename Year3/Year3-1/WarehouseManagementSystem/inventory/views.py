
from accounts.models import UserProfile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,  render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, ItemAttribute, StockRecord



def index(request):

    user = request.user


    if user.userprofile.role == "ADMIN":

        pending_count = UserProfile.objects.filter(
            status="PENDING"
        ).count()


        return render(
            request,
            "inventory/admin_index.html",
            {
                "pending_count": pending_count
            }
        )


    else:

        return redirect(
            "inventory_list"
        )




def inventory_list(request):

    items = Item.objects.all()


    return render(
        request,
        "inventory/inventory_list.html",
        {
            "items":items
        }
    )



def create_item(request):

    # 权限检查
    if request.user.userprofile.role != "ADMIN":

        return HttpResponse(
            "没有权限!"
        )


    if request.method == "POST":

        name = request.POST["name"]

        category = request.POST.get(
            "category",
            ""
        )

        quantity = int(
            request.POST["quantity"]
        )

        location = request.POST.get(
            "location",
            ""
        )


        # =====================
        # 获取上传图片
        # =====================

        image = request.FILES.get(
            "location_image"
        )


        # =====================
        # 1. 创建物品
        # =====================

        item = Item.objects.create(

            name=name,

            category=category,

            quantity=quantity,

            location=location,

            created_by=request.user

        )


        # =====================
        # 2. 保存动态属性
        # =====================

        keys = request.POST.getlist(
            "attribute_key"
        )


        values = request.POST.getlist(
            "attribute_value"
        )


        for key, value in zip(keys, values):

            if key and value:

                ItemAttribute.objects.create(

                    item=item,

                    key=key,

                    value=value

                )


        # =====================
        # 3. 创建首次入库记录
        # =====================

        StockRecord.objects.create(

            user=request.user,

            item=item,

            type="IN",

            quantity=quantity,

            reason="首次入库",

            location_image=image

        )


        return redirect(
            "inventory_list"
        )


    return render(
        request,
        "inventory/create_item.html"
    )


def item_detail(request,id):
    item = get_object_or_404(
        Item,
        id=id
    )

    return render(
        request,
        "inventory/item_detail.html",
        {
            "item":item
        }
    )







@login_required
def stock_in(request,id):


    # 权限检查

    if request.user.userprofile.role != "ADMIN":

        return HttpResponse(
            "没有权限"
        )


    item = get_object_or_404(
        Item,
        id=id
    )


    if request.method == "POST":


        quantity = int(
            request.POST["quantity"]
        )


        reason = request.POST.get(
            "reason",
            ""
        )


        image = request.FILES.get(
            "location_image"
        )


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

            location_image=image

        )


        return redirect(
            "item_detail",
            id=item.id
        )



    return render(
        request,
        "inventory/stock_in.html",
        {
            "item":item
        }
    )



def increase_stock(request,id):


    # 权限

    if request.user.userprofile.role != "ADMIN":

        return HttpResponse(
            "没有权限"
        )


    item = Item.objects.get(
        id=id
    )



    if request.method == "POST":


        quantity = int(
            request.POST["quantity"]
        )


        reason = request.POST.get(
            "reason",
            ""
        )


        image = request.FILES.get(
            "location_image"
        )


        # 修改库存

        item.quantity += quantity

        item.save()



        # 创建记录

        StockRecord.objects.create(

            user=request.user,

            item=item,

            type="IN",

            quantity=quantity,

            reason=reason,

            location_image=image

        )


        return redirect(
            "item_detail",
            id=item.id
        )



    return render(
        request,
        "inventory/increase_stock.html",
        {
            "item":item
        }
    )