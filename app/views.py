from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from app.color_picker import get_best_color
from .models import Singer, Album, PlayList
from .services import toggleSongInPlayList, toggleSongLike, toggleAlbumLike
from .serializers import (
   PlayListDetailSerializer, PlayListSerializer,
   SingerDetailSerializer, AlbumDetailSerializer, SmallPlayListSerializer,
)


class SingerDetailView(generics.RetrieveAPIView):
   queryset = Singer.objects.all()
   serializer_class = SingerDetailSerializer


class AlbumDetailView(generics.RetrieveAPIView):
   queryset = Album.objects.all()
   serializer_class = AlbumDetailSerializer


class PlayListsView(generics.ListAPIView):
   serializer_class = SmallPlayListSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user).order_by('-id')


class PlayListDetailView(generics.RetrieveAPIView):
   serializer_class = PlayListDetailSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user)


class PlayListCreateView(generics.CreateAPIView):
   serializer_class = PlayListSerializer


class PlayListDeleteView(generics.DestroyAPIView):
   serializer_class = PlayListSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user)


class PlayListUpdateView(generics.UpdateAPIView):
   serializer_class = PlayListSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user)


class AddSongView(APIView):
   def post(self, request):
      return toggleSongInPlayList(request, mode='add')


class RemoveSongView(APIView):
   def post(self, request):
      return toggleSongInPlayList(request, mode='remove')


class ToggleSongLikeView(APIView):
   def post(self, request):
      return toggleSongLike(request)

   
class ToggleAlbumLikeView(APIView):
   def post(self, request):
      return toggleAlbumLike(request)