# Generated by Django 4.2.3 on 2023-07-15 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together={('username', 'email')},
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
    ]
