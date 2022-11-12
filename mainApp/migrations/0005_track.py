# Generated by Django 4.1.3 on 2022-11-05 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_alter_myuser_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songName', models.CharField(blank=True, max_length=20, null=True)),
                ('song_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.myuser')),
            ],
        ),
    ]