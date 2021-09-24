# Generated by Django 3.2.6 on 2021-08-20 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='album name')),
                ('year', models.SmallIntegerField()),
                ('photo', models.ImageField(upload_to='albums_photos/', verbose_name='album photo file')),
                ('best_color', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='CustomManyToManyForTrackingTimeInserted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_inserted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='genre name')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='name')),
                ('audio', models.FileField(upload_to='songs_audio/', verbose_name='audio file')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='app.album', verbose_name='album')),
            ],
        ),
        migrations.CreateModel(
            name='SongLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='singer name')),
                ('photo', models.ImageField(null=True, upload_to='singers_photos/', verbose_name='singer photo file')),
                ('genres', models.ManyToManyField(to='app.Genre', verbose_name='singer genres list')),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='playlist name')),
                ('songs', models.ManyToManyField(blank=True, through='app.CustomManyToManyForTrackingTimeInserted', to='app.Song', verbose_name='playlist songs list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user who created playlist')),
            ],
        ),
        migrations.AddField(
            model_name='custommanytomanyfortrackingtimeinserted',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.playlist'),
        ),
        migrations.AddField(
            model_name='custommanytomanyfortrackingtimeinserted',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.song'),
        ),
        migrations.CreateModel(
            name='AlbumLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='app.album')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='album',
            name='singer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='app.singer', verbose_name='singer who wrote the album'),
        ),
    ]
