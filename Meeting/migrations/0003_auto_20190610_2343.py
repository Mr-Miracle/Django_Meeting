# Generated by Django 2.2.1 on 2019-06-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Meeting', '0002_auto_20190610_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parks',
            name='code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='parks',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='parks',
            name='place',
            field=models.CharField(max_length=50),
        ),
    ]
