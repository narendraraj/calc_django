# Generated by Django 3.1.4 on 2022-04-16 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d_spacing', '0006_auto_20220416_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='crystaldata',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
