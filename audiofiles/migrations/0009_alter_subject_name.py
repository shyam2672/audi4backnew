# Generated by Django 4.2.1 on 2024-02-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiofiles', '0008_remove_subject_unique_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
