from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework.response import Response
from .models import Album, AlbumLike, PlayList, Singer, SingerLike, Song, SongLike
from .serializers import TogggleSongInPlaylistSerializer, TogggleLikeSerializer
from .functions import format_album_duration


# todo: don't return responses from services

def _get_or_create_like(user, id, model_class, like_model_class):
   model_instance = get_object_or_404(model_class, pk=id)
   like, created = like_model_class.objects.get_or_create(user=user, instance=model_instance)
   return like, created

def _like_switcher_creator(model_class, like_model_class):
   def switcher(request):
      serializer = TogggleLikeSerializer(data=request.data)
      if serializer.is_valid():
         like, created = _get_or_create_like(
            user=request.user,
            id=serializer.validated_data.get('id'),
            model_class=model_class,
            like_model_class=like_model_class,
         )
         if created:
            return Response(serializer.data, status=201)
         else:
            like.delete()
            return Response(serializer.data, status=200)
      return HttpResponse(status=400)

   return switcher


switch_song_like = _like_switcher_creator(Song, SongLike)

switch_album_like = _like_switcher_creator(Album, AlbumLike)

switch_singer_like = _like_switcher_creator(Singer, SingerLike)


def switchSongInPlayList(request, mode):
   serializer = TogggleSongInPlaylistSerializer(data=request.data)
   if serializer.is_valid():
      playlist = get_object_or_404(
         PlayList,
         pk=serializer.validated_data.get('playlist_id'),
         user=request.user,
      )
      song = get_object_or_404(Song, pk=serializer.validated_data.get('song_id'))
      if mode == 'add':
         playlist.songs.add(song)
      elif mode == 'remove':
         playlist.songs.remove(song)
      return Response({ 'id': song.id }, status=201)
   return HttpResponse(status=400)