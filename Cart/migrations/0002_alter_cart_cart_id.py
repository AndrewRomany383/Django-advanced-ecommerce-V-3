# Generated by Django 4.2.7 on 2023-12-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(max_length=300, null=True, unique=True),
        ),
    ]