# Generated by Django 4.2 on 2024-06-08 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_processstaffattendancemst_staff_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='processstaffattendancemst',
            name='staff_payroll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staffpayroll'),
        ),
    ]