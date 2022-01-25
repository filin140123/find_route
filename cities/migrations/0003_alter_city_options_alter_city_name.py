# Generated by Django 4.0 on 2022-01-25 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_alter_city_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name'], 'verbose_name': 'город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='город'),
        ),
    ]