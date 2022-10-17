# Generated by Django 4.1.2 on 2022-10-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_remove_exam_course_or_category_remove_exam_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='categories',
            field=models.ManyToManyField(blank=True, to='courses.category'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='related_courses',
            field=models.ManyToManyField(blank=True, to='courses.course'),
        ),
    ]
