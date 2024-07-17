# Generated by Django 4.2 on 2024-07-16 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0003_rename_activestatue_activestatus'),
        ('staff', '0014_staffstatustransaction_staff_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.contracttype'),
        ),
    ]