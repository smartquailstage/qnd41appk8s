# Generated by Django 4.2.6 on 2024-01-08 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbmshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sbmproduct',
            name='conditions',
            field=models.TextField(blank=True),
        ),
    ]
