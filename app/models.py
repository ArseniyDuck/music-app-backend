from app.color_picker import get_best_color
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
   name = models.CharField(max_length=240, verbose_name='genre name')

   def __str__(self):
      return self.name


class Singer(models.Model):
   name = models.CharField(max_length=240, verbose_name='singer name')
   photo = models.ImageField(upload_to='singers_photos/', null=True, verbose_name='singer photo file')
   genres = models.ManyToManyField(to=Genre, verbose_name='singer genres list')

   def __str__(self):
      return self.name


class Album(models.Model):
   name = models.CharField(max_length=240, verbose_name='album name')
   year = models.SmallIntegerField()
   photo = models.ImageField(upload_to='albums_photos/', verbose_name='album photo file')
   best_color = models.CharField(max_length=18)
   singer = models.ForeignKey(to=Singer, on_delete=models.CASCADE, related_name='albums', verbose_name='singer who wrote the album')

   def save(self, *args, **kwargs):
      # todo: accumulate duration in save method
      if not self.id:
         self.best_color = get_best_color(self.photo)
      super(Album, self).save(*args, **kwargs)

   def __str__(self):
      return self.name


class Song(models.Model):
   """
      A song is a musical composition, which metadata (eg. duration) is readed and displayed by JavaScript.
      It can't be created outside an album. Therefore singers can't have singles (single can only exist in an album).
   """
   name = models.CharField(max_length=240, verbose_name='name')
   album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='songs', verbose_name='album')
   audio = models.FileField(upload_to='songs_audio/', verbose_name='audio file')
   # todo: get duration in save method with "if not self.id"

   def __str__(self):
      return self.name


class PlayList(models.Model):
   """
      Users can create their own playlists and fill them with any songs.
      !!!Generated or admin-made playlists (eg. 'for the mood', 'déjà vu' or 'popular songs') are NOT SUPPORTED!!!
   """
   # todo: add photo field to PlayList
   name = models.CharField(max_length=240, verbose_name='playlist name')
   songs = models.ManyToManyField(
      to=Song,
      through='CustomManyToManyForTrackingTimeInserted',
      blank=True,
      verbose_name='playlist songs list'
   )
   user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='user who created playlist')

   def get_ordered_songs(self):
      return self.songs.all().order_by('custommanytomanyfortrackingtimeinserted__time_inserted')

   def get_photo(self):
      first_song = self.get_ordered_songs().first()
      if first_song:
         return first_song.album.photo.url
      return None
         

   def __str__(self):
      return self.name

class CustomManyToManyForTrackingTimeInserted(models.Model):
   song = models.ForeignKey(to=Song, on_delete=models.CASCADE)
   playlist = models.ForeignKey(to=PlayList, on_delete=models.CASCADE)
   time_inserted = models.DateTimeField(auto_now_add=True)


class AbstractLike(models.Model):
   user = models.ForeignKey(to=User, on_delete=models.CASCADE)

   class Meta:
      abstract = True


class SongLike(AbstractLike):
   instance = models.ForeignKey(to=Song, on_delete=models.CASCADE, related_name='likes')

   def __str__(self):
      return f'{self.user.name}\'s like of song {self.song.name}'


class AlbumLike(AbstractLike):
   instance = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='likes')

   def __str__(self):
      return f'{self.user.name}\'s like of song {self.album.name}'