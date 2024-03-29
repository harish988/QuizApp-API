# Generated by Django 2.1.15 on 2020-06-05 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Answer', verbose_name='answer')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='question')),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Quiz', verbose_name='quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile', verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'User Answers',
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('is_pass', models.BooleanField(default=False)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Quiz', verbose_name='quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile', verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'User Scores',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userscore',
            unique_together={('user', 'quiz_id')},
        ),
    ]
