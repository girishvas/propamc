# Generated by Django 2.2.6 on 2019-10-24 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('address', models.CharField(blank=True, max_length=600, null=True)),
                ('latitude', models.CharField(blank=True, max_length=40, null=True)),
                ('longitude', models.CharField(blank=True, max_length=40, null=True)),
                ('added_On', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_On', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
    ]