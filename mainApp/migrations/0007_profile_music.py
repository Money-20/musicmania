# Generated by Django 4.1.3 on 2022-11-07 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_remove_myuser_mobile_remove_myuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='music',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.track'),
        ),
    ]