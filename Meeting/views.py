"""django 视图模块，通过它可以把用户请求的页面调出来。"""

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User  # django 自带后台管理模块
from django.contrib import auth
from Meeting.models import *


# 主页
def index(req):
    username = req.session.get('username', '')
    content = {'active_menu': 'homepage', 'user': username}
    return render_to_response('index.html', content)  # 将数据返回到前台


# 注册
def register(req):
    if req.session.get('username', ''):  # 获取session用来判断用户是否登录
        return HttpResponseRedirect('/')
    state = ""
    if req.POST:
        username = req.POST.get("username", "")  # 从前台获得用户注册信息，判断，存入数据库
        if User.objects.filter(username=username):
            state = "user_exist"
        else:
            password = req.POST.get("password", "")
            repassword = req.POST.get("repassword", "")
            if password != repassword:
                state = "re_err"
            else:
                newuser = User.objects.create_user(username=username, password=password)
                newuser.save()
                new_myuser = MyUser(username=newuser, phone=req.POST.get("phone"))
                new_myuser.save()
                state = "success"
                return HttpResponseRedirect("/login/")
    return render(request=req, template_name='register.html', status=200, context={"active_menu": "homepage", "state": state, "user": ""}, )


# 登录
def login(req):
    if req.session.get('username', ''):
        return HttpResponseRedirect('/')
    state = ""
    if req.POST:
        username = req.POST.get("username", "")
        password = req.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            req.session["username"] = username  # 保存登录会话
            return HttpResponseRedirect('/')
        else:
            state = "is_not_exist"
    return render(request=req, template_name='login.html', status=200, context={"state": state})


# 退出登录
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')


# 获取学院列表
def get_acad_list():
    room_list = ConfeRoom.objects.all()  # 对数据库的操作
    acad_list = set()
    for room in room_list:
        acad_list.add(room.acad)
    return list(acad_list)


# 查看会议室
def view_room(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    acad_list = get_acad_list()
    room_acad = req.GET.get("acad", "all")  # 从前台点击选择学院，
    if room_acad not in acad_list:  # 如果没有就全部显示
        room_acad = "all"
        room_list = ConfeRoom.objects.all()
    else:
        room_list = ConfeRoom.objects.filter(acad=room_acad)  # 只显示选定学院的会议室
    content = {"active_menu": 'view_room', "acad_list": acad_list, "room_acad": room_acad, "room_list": room_list,
               "user": user}
    # return render_to_response('view_room.html', content, context_instance=RequestContext(req))
    return render(request=req, template_name='view_room.html', status=200, context=content)


# 会议室详情
def detail(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = req.GET.get("id", "")  # 获得会议室主键ID号
    req.session["id"] = Id
    if Id == "":
        return HttpResponseRedirect('/view_room/')
    try:
        room = ConfeRoom.objects.get(pk=Id)  # 根据ID显示详细信息
        ro = Detail.objects.get(pk=Id)
    except:
        return HttpResponseRedirect('/view_room/')
    img_list = Detail.objects.filter(room=room)
    num_list = get_order_list()
    if room.num not in num_list:  # 判断是否被预定，给定状态，给前台显示是否可以预定
        or_sta = "yes"
    else:
        or_sta = "no"
    content = {"active_menu": "view_room", "room": room, "img_list": img_list, "ro": ro, "or_sta": or_sta, "user": user}
    # return render_to_response('detail.html', content)
    return render(request=req, template_name='detail.html', status=200, context=content)


# 预定
# 获取预定列表
def order(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    row_id = req.session.get("id", "")  # 预定，将数据保存到数据库
    room = ConfeRoom.objects.get(pk=row_id)
    time = Detail.objects.get(name=room.name)
    u = MyUser.objects.get(user__username=username)
    order0 = Order(user=username, num=room.num, name=room.name, time=time.time, size=room.size, phone=u.phone)
    order0.save()
    # return render_to_response("index2.html", {"user": user}, context_instance=RequestContext(req))
    return render(request=req, template_name='index2.html', status=200, context={"user": user})


def get_order_list():
    num_list = set()
    order_list = Order.objects.all()
    for order0 in order_list:
        num_list.add(order0.num)
    return list(num_list)


# 查看预定信息
def my_orders(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    try:
        my_order = Order.objects.all()  # 索引数据库查看已预订信息
        us_sta = "no"
        return render(request=req, template_name='my_orders.html', status=200, context={"my_order": my_order, "us_sta": us_sta, "user": user})
    except MyUser:
        us_sta = "yes"
        return render(request=req, template_name='my_orders.html', status=200, context={"my_order": my_order, "us_sta": us_sta, "user": user})


# 取消预定
def cancel(req):
    username = req.session.get('username', '')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = req.GET.get("id", "")  # 取消预订，删除数据
    room = Order.objects.get(pk=Id)
    room.delete()
    # return render_to_response("index.html", context_instance=RequestContext(req))
    return render(request=cancel(), template_name='index.html', context={"user": user})




