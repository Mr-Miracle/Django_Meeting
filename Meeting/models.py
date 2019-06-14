"""python 模型，一个模型对应数据库的一个表。模型中的每一个属性对应数据库表的字段。"""
from django.db import models
# Create your models here.


class Users(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Rooms(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    floor = models.CharField(max_length=20)
    capacity = models.CharField(max_length=20)
    equipment = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Orders(models.Model):
    theme = models.CharField(max_length=20)
    room = models.CharField(max_length=20)
    creator = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    partner = models.CharField(max_length=100)
    orderdate = models.DateTimeField(max_length=20)
    starttime = models.DateTimeField(max_length=20)
    endtime = models.DateTimeField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Parks(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


