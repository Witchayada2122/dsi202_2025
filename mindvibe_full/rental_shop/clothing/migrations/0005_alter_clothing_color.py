# Generated by Django 5.1.6 on 2025-04-20 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0004_alter_clothing_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothing',
            name='color',
            field=models.CharField(default='N/A', max_length=20),
        ),
    ]
