from django.contrib import admin
from .models import Singer, Album, PlayList, Song, Genre, SongLike

admin.site.register(PlayList)
admin.site.register(Song)
admin.site.register(Genre)


class SingerAdmin(admin.ModelAdmin):
   filter_horizontal = ('genres', )
admin.site.register(Singer, SingerAdmin)


class SongInline(admin.TabularInline):
   model = Song
   extra = 1

class AlbumAdmin(admin.ModelAdmin):
   fields = ('name', 'year', 'photo', 'singer')
   inlines = (SongInline, )
admin.site.register(Album, AlbumAdmin)