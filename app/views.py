import re
from django.contrib.auth.models import User
from django.http import request
from rest_framework import generics, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from app.color_picker import get_best_color
from .models import Singer, Album, PlayList
from .services import toggleSongInPlayList, toggleSongLike, toggleAlbumLike
from .serializers import (
   LikedSongsPlaylistSerializer, PlayListDetailSerializer, PlayListSerializer, RegisterSerializer,
   SingerDetailSerializer, AlbumDetailSerializer, SmallAlbumListSeriailizer, SmallPlayListSerializer, SongSerializer, UserSerializer,
)


class SingerDetailView(generics.RetrieveAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   queryset = Singer.objects.all()
   serializer_class = SingerDetailSerializer


class AlbumDetailView(generics.RetrieveAPIView):
   authentication_classes = (JWTAuthentication, )
   permission_classes = (AllowAny, ) 
   queryset = Album.objects.all()
   serializer_class = AlbumDetailSerializer


class PlayListsView(generics.ListAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   serializer_class = SmallPlayListSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user).order_by('-id')


class AlbumsView(generics.ListAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   serializer_class = SmallAlbumListSeriailizer
   def get_queryset(self):
      return [i.instance for i in self.request.user.albumlike_set.all()]


class PlayListDetailView(generics.RetrieveAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   serializer_class = PlayListDetailSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user)


class PlayListCreateView(generics.CreateAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   serializer_class = PlayListSerializer


class PlayListDeleteView(generics.DestroyAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   serializer_class = PlayListSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user)


class PlayListUpdateView(generics.UpdateAPIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   serializer_class = PlayListSerializer
   def get_queryset(self):
      return PlayList.objects.filter(user=self.request.user)


class AddSongView(APIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   def post(self, request):
      return toggleSongInPlayList(request, mode='add')


class RemoveSongView(APIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   def post(self, request):
      return toggleSongInPlayList(request, mode='remove')


class ToggleSongLikeView(APIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   def post(self, request):
      return toggleSongLike(request)

   
class ToggleAlbumLikeView(APIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   def post(self, request):
      return toggleAlbumLike(request)


class LikedSongsView(APIView):
   permission_classes = (IsAuthenticated, )
   authentication_classes = (JWTAuthentication, )
   def get(self, request):
      serializer = LikedSongsPlaylistSerializer(request.user, context={'request': request})
      return Response(serializer.data)


@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def user(request: Request):
   serializer = UserSerializer(request.user)
   return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
   queryset = User.objects.all()
   permission_classes = (AllowAny,)
   serializer_class = RegisterSerializer