"""django 视图模块，通过它可以把用户请求的页面调出来。"""

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from Meeting.models import *


# 首页
def index(req):
    username = req.session.get('username', '')
    content = {'active_menu': 'homepage', 'user': username}
    return render_to_response('index.html', content)  # 将数据返回到前台


# 注册
def register(req):
    if req.session.get('email', ''):  # 获取session用来判断用户是否登录
        return HttpResponseRedirect('/')

    email = req.POST.get("email", "")
    if Users.objects.filter(email=email):
        state = "user_exist"
    else:
        password = req.POST.get("password", "")
        repassword = req.POST.get("repassword", "")
        if password != repassword:
            state = "re_err"
        else:
            username = req.POST.get("username", "")
            phone = req.POST.get("phone", "")
            new_user = Users.objects.create(email=email, password=password, username=username, phone=phone)
            new_user.save()
            return HttpResponseRedirect("/login/")

    return render(request=req, template_name='register.html', status=200, context={"active_menu": "index", "state": state, "username": ""}, )


# 登录
def login(req):
    if req.session.get('usr', ''):
        return HttpResponseRedirect('/index/')
    state = ""
    if req.POST:
        email = req.POST.get("email", "")
        password = req.POST.get("password", "")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(req, user)
            req.session["user"] = user  # 保存登录会话
            return HttpResponseRedirect('/index/')
        else:
            state = "is_not_exist"
    return render(request=req, template_name='login.html', status=200, context={"state": state})


# 退出登录
def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/')


# 获取园区列表
def get_park_list():
    room_list = Parks.objects.all()  # 对数据库的操作
    park_list = set()
    for room in room_list:
        park_list.add(room.code)
    return list(park_list)


# 查看会议室
def view_room(req):
    username = req.session.get('username', '')
    if username != '':
        user = Users.objects.get(username=username)
    else:
        user = ''
    park_list = get_park_list()
    room_park = req.GET.get("park", "all")  # 从前台点击选择学院，
    if room_park not in park_list:  # 如果没有就全部显示
        room_park = "all"
        room_list = Parks.objects.all()
    else:
        room_list = Parks.objects.filter(acad=room_park)  # 只显示选定学院的会议室
    content = {"active_menu": 'view_room', "park_list": park_list, "room_park": room_park, "room_list": room_list,
               "user": user}
    return render(request=req, template_name='view_room.html', status=200, context=content)


# 会议室详情
def detail(req):
    username = req.session.get('username', '')
    if username != '':
        user = Users.objects.get(username=username)
    else:
        user = ''
    Id = req.GET.get("id", "")  # 获得会议室主键ID号
    req.session["id"] = Id
    if Id == "":
        return HttpResponseRedirect('/view_room/')
    try:
        room = Rooms.objects.get(pk=Id)  # 根据ID显示详细信息
        ro = Orders.objects.get(pk=Id)
    except:
        return HttpResponseRedirect('/view_room/')
    img_list = Orders.objects.filter(room=room)
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
        user = Users.objects.get(username=username)
    else:
        user = ''
    row_id = req.session.get("id", "")  # 预定，将数据保存到数据库
    room = Rooms.objects.get(pk=row_id)
    time = Orders.objects.get(room=room.name)
    user0 = Users.objects.get(username=username)
    order0 = Orders(user=username, num=room.num, name=room.name, time=time.time, size=room.capacity, phone=user0.phone)
    order0.save()
    return render(request=req, template_name='index2.html', status=200, context={"user": user})


def get_order_list():
    num_list = set()
    order_list = Orders.objects.all()
    for order0 in order_list:
        num_list.add(order0.num)
    return list(num_list)


# 查看预定信息
def my_orders(req):
    username = req.session.get('username', '')
    if username != '':
        user = Users.objects.get(username=username)
    else:
        user = ''

    try:
        my_order = Orders.objects.all()  # 索引数据库查看已预订信息
        us_sta = "no"
        return render(request=req, template_name='my_orders.html', status=200, context={"my_order": my_order, "us_sta": us_sta, "user": user})
    except Users:
        us_sta = "yes"
    return render(request=req, template_name='my_orders.html', status=200, context={"my_order": my_order, "us_sta": us_sta, "user": user})


# 取消预定
def cancel(req):
    username = req.session.get('username', '')
    if username != '':
        user = Users.objects.get(username=username)
    else:
        user = ''
    Id = req.GET.get("id", "")  # 取消预订，删除数据
    room = Orders.objects.get(pk=Id)
    room.delete()
    # return render_to_response("index.html", context_instance=RequestContext(req))
    return render(request=cancel(), template_name='index.html', context={"user": user})




