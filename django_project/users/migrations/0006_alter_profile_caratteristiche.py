# Generated by Django 5.0.4 on 2024-05-16 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_cognome_remove_profile_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='caratteristiche',
            field=models.CharField(blank=True, choices=[('nessuna', 'Nessuna'), ('dsa', 'DSA'), ('invalido', 'Invalido'), ('allergico', 'Allergico')], max_length=100, null=True),
        ),
    ]
