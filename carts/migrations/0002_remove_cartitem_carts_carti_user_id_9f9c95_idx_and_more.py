# Generated by Django 4.1 on 2022-08-10 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='cartitem',
            name='carts_carti_user_id_9f9c95_idx',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart_id',
            field=models.CharField(blank=True, max_length=60, unique=True),
        ),
        migrations.AddIndex(
            model_name='cartitem',
            index=models.Index(fields=['item', 'quantity', 'total_price', 'cart_id'], name='carts_carti_item_id_e308d2_idx'),
        ),
    ]
