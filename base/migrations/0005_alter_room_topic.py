# Generated by Django 4.2.3 on 2023-07-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_topic_room_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='topic',
            field=models.ManyToManyField(related_name='topic_rooms', to='base.topic'),
        ),
    ]
