# Generated by Django 5.1.3 on 2024-11-25 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questify_app', '0003_modulpembelajaran_gratis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaksi',
            name='total_pembayaran',
        ),
        migrations.AddField(
            model_name='transaksi',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
