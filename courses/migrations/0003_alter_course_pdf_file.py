# Generated by Django 4.1.2 on 2022-10-09 16:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_video-or-pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='courses', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
