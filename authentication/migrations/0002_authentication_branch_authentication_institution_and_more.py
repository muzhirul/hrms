# Generated by Django 4.2 on 2024-05-22 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
        ('setup_app', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authentication',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch'),
        ),
        migrations.AddField(
            model_name='authentication',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution'),
        ),
        migrations.AddField(
            model_name='authentication',
            name='role',
            field=models.ManyToManyField(related_name='user_role', to='setup_app.role'),
        ),
    ]