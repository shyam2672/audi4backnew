# Generated by Django 4.2.1 on 2024-02-18 14:25

import audiofiles.models
from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('audiofiles', '0002_audiofiles_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Chapter',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'subjects',
            },
        ),
        migrations.AlterField(
            model_name='audiofiles',
            name='AudioFile',
            field=models.FileField(null=True, storage=gdstorage.storage.GoogleDriveStorage(permissions=(gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['WRITER'], gdstorage.storage.GoogleDrivePermissionType['USER'], '2020csb1110@iitrpr.ac.in'), gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['WRITER'], gdstorage.storage.GoogleDrivePermissionType['USER'], '2020csb1107@iitrpr.ac.in'))), upload_to=audiofiles.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='audiofiles',
            name='PDF',
            field=models.FileField(null=True, storage=gdstorage.storage.GoogleDriveStorage(permissions=(gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['WRITER'], gdstorage.storage.GoogleDrivePermissionType['USER'], '2020csb1110@iitrpr.ac.in'), gdstorage.storage.GoogleDriveFilePermission(gdstorage.storage.GoogleDrivePermissionRole['WRITER'], gdstorage.storage.GoogleDrivePermissionType['USER'], '2020csb1107@iitrpr.ac.in'))), upload_to=audiofiles.models.file_path),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.IntegerField(unique=True)),
                ('subjects', models.ManyToManyField(null=True, to='audiofiles.subject')),
            ],
            options={
                'verbose_name_plural': 'Grades',
            },
        ),
        migrations.CreateModel(
            name='Chapters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chapters', models.ManyToManyField(null=True, to='audiofiles.chapter')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audiofiles.grade')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audiofiles.subject')),
            ],
            options={
                'verbose_name_plural': 'Chapters',
            },
        ),
    ]
