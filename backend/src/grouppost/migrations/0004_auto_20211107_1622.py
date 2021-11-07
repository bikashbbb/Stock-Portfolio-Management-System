# Generated by Django 2.1.5 on 2021-11-07 16:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grouppost', '0003_allposts_post_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='bannedusers',
            field=models.ManyToManyField(blank=True, default=None, related_name='bannuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='allposts',
            name='post_comments',
            field=models.ManyToManyField(blank=True, default=None, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='allposts',
            name='post_dislikes',
            field=models.ManyToManyField(blank=True, default=None, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
