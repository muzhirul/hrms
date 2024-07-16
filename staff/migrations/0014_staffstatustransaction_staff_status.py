# Generated by Django 4.2 on 2024-07-16 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0003_rename_activestatue_activestatus'),
        ('staff', '0013_staff_staff_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffstatustransaction',
            name='staff_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.activestatus'),
        ),
    ]