# Generated by Django 4.2 on 2024-12-04 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_staff_staff_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='staff_no',
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
