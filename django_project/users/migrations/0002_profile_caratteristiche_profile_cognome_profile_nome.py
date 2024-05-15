# Generated by Django 5.0.4 on 2024-05-15 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='caratteristiche',
            field=models.CharField(blank=True, choices=[('dsa', 'DSA'), ('disabile', 'Disabile'), ('allergico', 'Allergico')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='cognome',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='nome',
            field=models.CharField(default='', max_length=100),
        ),
    ]
