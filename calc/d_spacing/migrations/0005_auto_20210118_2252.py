# Generated by Django 3.1.4 on 2021-01-18 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('d_spacing', '0004_auto_20210110_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crystaldata',
            old_name='cell_lenght_a',
            new_name='cell_length_a',
        ),
        migrations.RenameField(
            model_name='crystaldata',
            old_name='cell_lenght_b',
            new_name='cell_length_b',
        ),
        migrations.RenameField(
            model_name='crystaldata',
            old_name='cell_lenght_c',
            new_name='cell_length_c',
        ),
    ]