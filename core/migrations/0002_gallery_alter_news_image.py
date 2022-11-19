# Generated by Django 4.1.3 on 2022-11-19 13:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('media', models.FileField(upload_to='gallery_files')),
                ('title', models.TextField()),
                ('is_video', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(upload_to='news_images'),
        ),
    ]
