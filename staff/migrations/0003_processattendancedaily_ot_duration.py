# Generated by Django 4.2 on 2024-05-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_attendancedailyraw_device_ip_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processattendancedaily',
            name='ot_duration',
            field=models.DurationField(blank=True, null=True, verbose_name='OT Duraion'),
        ),
    ]
