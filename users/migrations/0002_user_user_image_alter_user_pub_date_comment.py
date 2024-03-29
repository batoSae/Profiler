# Generated by Django 5.0.2 on 2024-02-23 13:37

import datetime
import django.db.models.deletion
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_image',
            field=models.ImageField(default='profile_pic/image.jpg', upload_to=users.models.image_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 23, 13, 37, 15, 379701, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(default='null', max_length=254)),
                ('body', models.TextField(default='null')),
                ('created_on', models.DateTimeField(verbose_name='date commented')),
                ('active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.user')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
