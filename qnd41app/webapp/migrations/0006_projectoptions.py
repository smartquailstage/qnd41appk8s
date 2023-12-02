# Generated by Django 4.2.6 on 2023-12-02 03:24

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_remove_galeriacreateitbusiness_image_10_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='projectoptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('project_description', wagtail.fields.RichTextField(blank=True, verbose_name='Descripcion de proyecto ')),
                ('project_title', models.CharField(blank=True, max_length=150, null=True, verbose_name='titulo de Projecto')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_descriptions', to='webapp.createprojects')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
