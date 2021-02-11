# Generated by Django 3.1.4 on 2021-01-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d_spacing', '0003_auto_20210110_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='crystaldata',
            name='comments',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='crystaldata',
            name='file_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]