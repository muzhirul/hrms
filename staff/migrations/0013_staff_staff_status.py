# Generated by Django 4.2 on 2024-07-16 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0003_rename_activestatue_activestatus'),
        ('staff', '0012_staffstatustransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='staff_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.activestatus'),
        ),
    ]
