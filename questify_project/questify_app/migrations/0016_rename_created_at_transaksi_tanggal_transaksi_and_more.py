# Generated by Django 5.1.3 on 2024-12-06 02:52

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questify_app', '0015_rename_tanggal_transaksi_transaksi_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaksi',
            old_name='created_at',
            new_name='tanggal_transaksi',
        ),
        migrations.RemoveField(
            model_name='transaksi',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='transaksi',
            name='status',
        ),
        migrations.AddField(
            model_name='transaksi',
            name='batas_waktu_pembayaran',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='transaksi',
            name='metode_pembayaran',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaksi', to='questify_app.metodepembayaran'),
        ),
        migrations.AddField(
            model_name='transaksi',
            name='status_pembayaran',
            field=models.CharField(choices=[('pending', 'Pending'), ('gagal', 'Gagal'), ('berhasil', 'Berhasil')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='kelas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi', to='questify_app.kelas'),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='link_payment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi', to=settings.AUTH_USER_MODEL),
        ),
    ]
