# Generated by Django 2.2.10 on 2020-05-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_quiz_no_of_question_to_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_correct_answer',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10),
        ),
    ]
