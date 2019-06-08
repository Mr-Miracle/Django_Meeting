"""python 模型，一个模型对应数据库的一个表。模型中的每一个属性对应数据库表的字段。"""
from django.db import models
# Create your models here.


class MyUser(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now_add=True)


class ConfeRoom(models.Model):
    list_display = ('pub_date', 'headline')
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()

    def __unicode__(self):
        return self.name


class Order(models.Model):
    list_display = ('pub_date', 'headline')
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()

    def __unicode__(self):
        return self.name


class Detail(models.Model):
    list_display = ('pub_date', 'headline')
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
#  reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name



