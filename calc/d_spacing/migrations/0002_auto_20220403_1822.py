# Generated by Django 3.1.4 on 2022-04-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d_spacing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crystaldata',
            name='space_group_IT_number',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='crystaldata',
            name='space_group_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]