# Generated by Django 5.0.4 on 2024-05-19 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gite', '0008_user_classe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_classe',
            options={'verbose_name_plural': 'User_classe'},
        ),
        migrations.RenameField(
            model_name='user_classe',
            old_name='User',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='user_classe',
            name='Classe',
        ),
        migrations.AddField(
            model_name='user_classe',
            name='classe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gite.classe'),
            preserve_default=False,
        ),
    ]