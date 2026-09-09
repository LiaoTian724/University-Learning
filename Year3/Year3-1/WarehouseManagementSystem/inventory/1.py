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
