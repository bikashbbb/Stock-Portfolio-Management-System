# Generated by Django 2.1.5 on 2021-10-31 08:07

from django.db import migrations, models
import hitcount.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('content', models.TextField(blank=True)),
                ('content_preview', models.TextField(blank=True)),
                ('category', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('recommended', models.BooleanField(default=False)),
                ('post_image_url', models.CharField(blank=True, max_length=120, null=True)),
                ('topRecommended', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=120)),
                ('lastName', models.CharField(max_length=120)),
                ('jobDescription_1', models.CharField(max_length=120)),
                ('jobDescription_2', models.CharField(max_length=120)),
                ('jobDescription_3', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('phone_1', models.CharField(blank=True, max_length=120)),
                ('phone_2', models.CharField(blank=True, max_length=120)),
                ('linkedin', models.URLField(blank=True)),
                ('github', models.URLField(blank=True)),
                ('wechat_QR_code', models.URLField(blank=True)),
            ],
        ),
    ]
