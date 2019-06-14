"""django 视图模块，通过它可以把用户请求的页面调出来。"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import *
from Meeting.models import *


# 首页
def index(req):
    if req.session.get('user'):
        return render(req, 'index.html')
    return redirect('/login/')


# 注册
def register(req):
    if req.method == 'GET':
        return render(req, 'register.html')
    if req.method == 'POST':
        id_email = req.POST.get("id_Email")
        id_name = req.POST.get("id_Name")
        # 判断用户输入的邮箱和用户名是否存在
        email = Users.objects.filter(email=id_email)
        name = Users.objects.filter(username=id_name)
        if email and name:
            message = '用户名或者邮箱已经被注册，请重新输入！'
            return render(req, 'register.html', {'message': message})
        else:
            id_password = req.POST.get("id_Password")
            id_phone = req.POST.get("id_Phone")
            new_DB_user = Users.objects.create(email=id_email, password=id_password, username=id_name, phone=id_phone)
            new_DB_User = User.objects.create_user(username=id_name, email=id_email, password=id_password)
            new_DB_user.save()
            new_DB_User.save()
            print(new_DB_User)
            message = '用户注册成功,请登录。'
            return render(req, 'login.html', {'message': message})


# 登录
def login(req):
    if req.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if req.method == 'GET':
        return render(req, 'login.html')
    if req.method == 'POST':
        name = req.POST.get('id_Username')
        passwd = req.POST.get('id_Password')
        message = '用户名或者密码为空！'
        if name.strip() and passwd:
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = Users.objects.get(username=name)
            except :
                message = '用户不存在！'
                return render(req, 'login.html', {'message': message})
            if user.password == passwd:
                req.session['is_login'] = True
                req.session['user'] = name
                return render(req, 'index.html', {'user': name})
            else:
                message = '密码不正确！'
                return render(req, 'login.html', {'message': message})
        else:
            return render(req, 'login.html', {'message': message})
    return render(req, 'login.html', {'message': '用户不存在或在密码错误，'})


# 退出登录
def logout(req):
    req.session.flush()
    return redirect('/login')


# 获取园区列表
def get_park_list():
    room_list = Parks.objects.all()  # 对数据库的操作
    park_list = set()
    for room in room_list:
        park_list.add(room.code)
    return list(park_list)


# 查看会议室

def view_room(req):
    if not req.session.get('user'):  # 限制未登录查看页面
        return redirect('/login')
    username = req.session.get('user')
    park_list = get_park_list()
    room_park = req.GET.get("park", "all")  # 从前台点击选择学院，
    if room_park not in park_list:  # 如果没有就全部显示
        room_park = "all"
        room_list = Rooms.objects.all()
    else:
        room_list = Rooms.objects.filter(room_park=room_park)  # 只显示选定学院的会议室
    content = {"active_menu": 'view_room', "park_list": park_list, "room_park": room_park, "room_list": room_list,
               "user": username}
    return render(request=req, template_name='view_room.html', context=content)


# 会议室详情
def detail(req):
    if not req.session.get('user'):  # 限制未登录查看页面
        return redirect('/login')
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


# 获取预定列表
def order(req):
    if not req.session.get('user'):  # 限制未登录查看页面
        return redirect('/login')
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
    if not req.session.get('user'):  # 限制未登录查看页面
        return redirect('/login')
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
    if not req.session.get('user'):  # 限制未登录查看页面
        return redirect('/login')
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




