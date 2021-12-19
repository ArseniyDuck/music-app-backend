from django.contrib.auth.models import User
from django.db import models
import mutagen
from rest_framework import fields, request, serializers
from .models import Album, Genre, PlayList, Singer, Song
from .functions import accumulate_songs_duration
from .color_picker import get_best_color
from .functions import format_song_duration, accumulate_songs_duration
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login
from itertools import chain


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
   is_liked = serializers.SerializerMethodField()
   songs = serializers.SerializerMethodField()
   albums = AlbumSerializer(many=True)
   likes_count = serializers.SerializerMethodField()

   def get_is_liked(self, obj):
      request = self.context['request']
      if request.user.is_authenticated:
         return bool(obj.likes.filter(user=request.user))

   def get_songs(self, obj):
      return PlaylistSongSerializer(
         list(chain(*[i.songs.all() for i in obj.albums.all()]))[:10],
         context = {'request': self.context['request']},
         many=True
      ).data

   def get_likes_count(self, obj):
      return obj.likes.count()


   class Meta:
      model = Singer
      fields = ('id', 'name', 'photo', 'genres', 'is_liked', 'likes_count', 'best_color', 'albums', 'songs', )


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
   photo = serializers.SerializerMethodField('get_photo')

   def get_songs_count(self, obj):
      return obj.songs.count()

   def get_photo(self, obj):
      return obj.get_photo()

   class Meta:
      model = PlayList
      fields = ('id', 'name', 'songs_count', 'photo', )


class SmallAlbumListSeriailizer(serializers.ModelSerializer):
   songs_count = serializers.SerializerMethodField()

   def get_songs_count(self, obj):
      return obj.songs.count()

   class Meta:
      model = Album
      fields = ('id', 'name', 'songs_count', 'photo')


class SmallSingerSerializer(serializers.ModelSerializer):
   genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

   class Meta:
      model = Singer
      fields = ('id', 'name', 'photo', 'genres', )


class SongSerializer(serializers.ModelSerializer):
   duration = serializers.SerializerMethodField()
   is_liked = serializers.SerializerMethodField()

   def get_duration(self, obj):
      audio_info = mutagen.File(obj.audio).info
      duration = int(audio_info.length)
      return format_song_duration(duration)

   def get_is_liked(self, obj):
      request = self.context['request']
      if request.user.is_authenticated:
         return bool(obj.likes.filter(user=request.user))

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
      request = self.context.get('request')
      if request.user.is_authenticated:
         return bool(obj.likes.filter(user=request.user))

   class Meta:
      model = Album
      fields = ('id', 'name', 'year', 'photo', 'best_color', 'is_liked', 'duration', 'singer', 'songs', )


class TogggleSongInPlaylistSerializer(serializers.Serializer):
   playlist_id = serializers.IntegerField()
   song_id = serializers.IntegerField()


class TogggleLikeSerializer(serializers.Serializer):
   id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ('id', 'username', )


class RegisterSerializer(serializers.ModelSerializer):
   password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
   password2 = serializers.CharField(write_only=True, required=True)

   class Meta:
      model = User
      fields = ('username', 'password1', 'password2', )

   def validate(self, attrs):
      if attrs['password1'] != attrs['password2']:
         raise serializers.ValidationError({'password1': 'Password fields didn\'t match.'})
      return attrs

   def create(self, validated_data):
      user = User.objects.create_user(validated_data['username'])
      user.set_password(validated_data['password1'])
      user.save()
      login(self.context['request'], user)
      return user


class LikedSongsPlaylistSerializer(serializers.ModelSerializer):
   songs = serializers.SerializerMethodField()
   duration = serializers.SerializerMethodField()

   def get_songs(self, obj):
      return PlaylistSongSerializer(
         reversed([i.instance for i in obj.songlike_set.all()]),
         context = {'request': self.context['request']},
         many=True
      ).data

   def get_duration(self, obj):
      return accumulate_songs_duration([i.instance for i in obj.songlike_set.all()])

   class Meta:
      model = User
      fields = ('username', 'songs', 'duration', )