# Generated by Django 4.1.3 on 2023-02-13 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_alter_projects_is_frozen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsinprojects',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]