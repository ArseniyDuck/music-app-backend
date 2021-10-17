from django.db import models
import mutagen
from rest_framework import fields, serializers
from .models import Album, PlayList, Singer, Song
from .functions import accumulate_songs_duration
from .color_picker import get_best_color
from .functions import format_song_duration, accumulate_songs_duration


class AlbumSerializer(serializers.ModelSerializer):
   class Meta:
      model = Album
      exclude = ('singer', )


class SingerSerializer(serializers.ModelSerializer):
   class Meta:
      model = Singer
      exclude = ('genres', )


class SingerDetailSerializer(serializers.ModelSerializer):
   genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
   albums = AlbumSerializer(many=True)

   class Meta:
      model = Singer
      fields = ('id', 'name', 'photo', 'genres', 'albums', )


class PlayListSerializer(serializers.ModelSerializer):
   def create(self, validated_data):
      return PlayList.objects.create(
         name = validated_data.get('name'),
         user = self.context['request'].user,
      )

   def update(self, instance, validated_data):
      instance.name = validated_data.get('name', instance.name)
      instance.save()
      return instance

   class Meta:
      model = PlayList
      fields = ('id', 'name', )

   
class SmallPlayListSerializer(serializers.ModelSerializer):
   songs_count = serializers.SerializerMethodField('get_songs_count')

   def get_songs_count(self, obj):
      return obj.songs.count()

   class Meta:
      model = PlayList
      fields = ('id', 'name', 'songs_count', )


class SongSerializer(serializers.ModelSerializer):
   duration = serializers.SerializerMethodField('get_duration')
   is_liked = serializers.SerializerMethodField('get_is_liked')

   def get_duration(self, obj):
      audio_info = mutagen.File(obj.audio).info
      duration = int(audio_info.length)
      return format_song_duration(duration)

   def get_is_liked(self, obj):
      return bool(obj.likes.filter(user=self.context.get('request').user))

   class Meta:
      model = Song
      fields = ('id', 'name', 'audio', 'duration', 'is_liked', )


class PlaylistSongSerializer(SongSerializer):
   album = AlbumSerializer()
   singer = serializers.SerializerMethodField('get_singer')
   
   def get_singer(self, obj):
      return {
         'id': obj.album.singer.id, 
         'name': obj.album.singer.name, 
      }

   class Meta(SongSerializer.Meta):
      fields = SongSerializer.Meta.fields + ('album', 'singer', )

   
class PlayListDetailSerializer(serializers.ModelSerializer):
   user = serializers.SlugRelatedField(slug_field='username', read_only=True)
   songs = PlaylistSongSerializer(source='get_ordered_songs', many=True)
   duration = serializers.SerializerMethodField('accumulate_duration')

   def accumulate_duration(self, obj):
      return accumulate_songs_duration(obj.songs.all())

   class Meta:
      model = PlayList
      fields = ('id', 'name', 'user', 'songs', 'duration', )


class AlbumDetailSerializer(serializers.ModelSerializer):
   singer = SingerSerializer()
   songs = SongSerializer(many=True)
   duration = serializers.SerializerMethodField('accumulate_duration')
   is_liked = serializers.SerializerMethodField('get_is_liked')

   def accumulate_duration(self, obj):
      return accumulate_songs_duration(obj.songs.all())

   def get_is_liked(self, obj):
      return bool(obj.likes.filter(user=self.context.get('request').user))

   class Meta:
      model = Album
      fields = ('id', 'name', 'year', 'photo', 'best_color', 'is_liked', 'duration', 'singer', 'songs', )


class TogggleSongInPlaylistSerializer(serializers.Serializer):
   playlist_id = serializers.IntegerField()
   song_id = serializers.IntegerField()


class TogggleLikeSerializer(serializers.Serializer):
   id = serializers.IntegerField()