# Generated by Django 4.2 on 2023-04-27 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_cart_is_active_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dish_name',
            field=models.CharField(default='Unnamed Dish', max_length=64),
        ),
        migrations.AddField(
            model_name='item',
            name='dish_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='item',
            name='dish',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.dish'),
        ),
    ]
