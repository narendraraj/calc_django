# Generated by Django 3.1.4 on 2022-05-14 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d_spacing', '0009_auto_20220418_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crystaldata',
            options={'ordering': ['-created']},
        ),
    ]
