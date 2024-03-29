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
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('site_or_quiz', models.CharField(choices=[('QUIZ', 'Quiz'), ('SITE', 'Site')], default='Quiz', max_length=5)),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5)),
                ('comments', models.CharField(max_length=2000, null=True)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Quiz', verbose_name='quiz')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile', verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Ratings',
                'db_table': 'rating',
                'managed': True,
            },
        ),
    ]
