# Generated by Django 2.2.10 on 2020-05-16 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20200516_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default='5', max_length=2),
        ),
        migrations.AlterField(
            model_name='rating',
            name='site_or_quiz',
            field=models.CharField(choices=[('QUIZ', 'Quiz'), ('SITE', 'Site')], default='QUIZ', max_length=5),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile', verbose_name='user'),
        ),
    ]
