# Generated by Django 3.2 on 2021-05-08 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('staff_no', models.IntegerField(default=0, unique=True)),
                ('houry_wage', models.IntegerField(default=1000)),
                ('counter_flg', models.BooleanField()),
                ('flyer_flg', models.BooleanField()),
                ('kitchen_flg', models.BooleanField()),
                ('responsible_flg', models.BooleanField()),
                ('opener_flg', models.BooleanField()),
                ('rookie_flg', models.BooleanField()),
                ('shift_creater_flg', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]