# Generated by Django 3.0.3 on 2020-02-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.IntegerField(default=0, verbose_name='조회수'),
        ),
    ]
