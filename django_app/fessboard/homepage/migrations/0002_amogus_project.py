# Generated by Django 4.1.3 on 2023-01-15 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='amogus',
            name='project',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='homepage.projects'),
            preserve_default=False,
        ),
    ]
