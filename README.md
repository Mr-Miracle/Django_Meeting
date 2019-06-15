python manage.py createsuperuser

$ python manage.py migrate   # 创建表结构

$ python manage.py makemigrations   # 让 Django 知道我们在我们的模型有一些变更
$ python manage.py migrate   # 创建表结构

9. startapp
django-admin startapp name [directory]

创建新的app。

默认情况下，会在这个新的app目录下创建一系列文件模版，比如models.py、views.py、admin.py等等。

10. startproject
django-admin startproject name [directory]

新建工程。默认情况下，新目录包含manage.py脚本和项目包（包含settings.py和其他文件）。

