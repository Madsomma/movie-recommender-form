# Generated by Django 3.1.3 on 2020-12-17 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=0)),
                ('movie_1', models.IntegerField(default=-1)),
                ('movie_2', models.IntegerField(default=-1)),
                ('movie_3', models.IntegerField(default=-1)),
                ('movie_4', models.IntegerField(default=-1)),
                ('rank_1', models.BooleanField()),
                ('rank_2', models.BooleanField()),
                ('rank_3', models.BooleanField()),
                ('rank_4', models.BooleanField()),
                ('date', models.DateTimeField(verbose_name='Date of survey')),
            ],
        ),
    ]