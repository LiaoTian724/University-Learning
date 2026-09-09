
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        real_name = request.POST["real_name"]
        password = request.POST["password"]


        # 登录名统一小写
        username = username.lower()

        # 检查p开头
        if not username.startswith("p"):
            return render(
                request,
                "accounts/register.html",
                {"error":"账号必须以P开头"}
            )
        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            profile = existing_user.userprofile

            if profile.status == "DISABLED":
                profile.status = "PENDING"
                profile.real_name = real_name
                profile.save()

                return render(request, "accounts/register_success.html",
                              {"message": "账号重新申请中，请等待管理员审核"})


            elif profile.status == "PENDING":
                return render(request, "accounts/register.html",
                              {"error": "该账号已经提交审核，请等待管理员处理"})

            else:
                return render(request, "accounts/register.html",
                              {"error": "该账号已经存在"})
        
        # 姓名格式化
        real_name = (real_name[0].upper()  +  real_name[1:].lower())
        if not real_name:
            return render(
                request,
                "accounts/register.html",
                {"error":"请输入姓名拼音"}
            )
        user = User.objects.create_user(
            username=username,
            password=password
        )


        UserProfile.objects.create(
            user=user,
            real_name=real_name,
            role="USER",   # 普通用户
            status="PENDING"  # 等待管理员审核
        )


        return redirect("login")


    return render(
        request,
        "accounts/register.html"
    )



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return render(
                request,
                "accounts/login.html",
                {"error":"用户名或密码错误"}
            )


            
        # 超级管理员直接登录
        if user.is_superuser:
            login(request, user)
            return redirect("/")

        profile = user.userprofile
        if profile.status == "DISABLED":
            return render(request,  "accounts/login.html",
                         {"error": "该账号已被禁用"})

        if profile.status != "APPROVED":
                return render( request, "accounts/login.html", 
                            {"error": "账号正在审核，请等待管理员批准"})

        login(request,user)
        return redirect("/")                    

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def approve_users(request):

    # 判断管理员
    profile = request.user.userprofile


    if profile.role != "ADMIN":

        return HttpResponse(
            "没有权限"
        )


    # 待审核
    pending_users = UserProfile.objects.filter(
        status="PENDING"
    )


    # 已审核历史
    checked_users = UserProfile.objects.exclude(
        status="PENDING"
    ).order_by(
        "-approved_time"
    )


    return render(
        request,
        "accounts/approve_users.html",
        {
            "pending_users": pending_users,
            "checked_users": checked_users
        }
    )


@login_required
def approve_user(request, username):

    profile = request.user.userprofile


    if profile.role != "ADMIN":

        return HttpResponse(
            "没有权限"
        )


    user_profile = UserProfile.objects.get(
        user__username=username
    )

    if user_profile.status != "PENDING":
        return HttpResponse(
            "该用户无需审核"
        )
    
    user_profile.status = "APPROVED"
    user_profile.approved_time = timezone.now()
    user_profile.save()


    return redirect(
        "approve_users"
    )


@login_required
def reject_user(request, username):

    profile = request.user.userprofile


    if profile.role != "ADMIN":

        return HttpResponse(
            "没有权限"
        )


    user_profile = UserProfile.objects.get(
        user__username=username
    )


    user_profile.status = "REJECTED"
    user_profile.approved_time = timezone.now()
    user_profile.save()


    return redirect(
        "approve_users"
    )



@login_required
def disable_user(request, username):
    if request.method != "POST":
        return HttpResponse("非法请求")

    profile = UserProfile.objects.get(user__username=username)

    profile.status="DISABLED"
    profile.save()

    return redirect("approve_users")


@login_required
def enable_user(request, username):
    if request.method != "POST":
        return HttpResponse("非法请求")

    profile = UserProfile.objects.get(user__username=username)
    profile.status = "APPROVED"

    profile.save()

    return redirect("approve_users")


@login_required
def change_role(request, username):
    
    if request.method != "POST":

        return HttpResponse(
            "非法请求"
        )


    # 当前操作者
    admin = request.user.userprofile


    if admin.role != "ADMIN":

        return HttpResponse(
            "没有权限"
        )


    profile = UserProfile.objects.get(
        user__username=username
    )

    if profile.user == request.user:
            return HttpResponse(
                "不能修改自己的权限"
            )
    
    if profile.role == "ADMIN":
        profile.role = "USER"


    else:

        profile.role = "ADMIN"


    profile.save()


    return redirect(
        "approve_users"
    )