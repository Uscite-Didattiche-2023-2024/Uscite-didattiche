# Generated by Django 5.0.3 on 2024-05-17 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_caratteristiche'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tipi_allergie',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
