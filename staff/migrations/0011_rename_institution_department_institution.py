# Generated by Django 4.2 on 2024-07-11 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0010_processstaffattendancemst_staff_payroll'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='Institution',
            new_name='institution',
        ),
    ]
