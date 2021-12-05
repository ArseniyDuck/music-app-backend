from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'app'
urlpatterns = [
   path('singer/<int:pk>/', SingerDetailView.as_view()),
   path('album/<int:pk>/', AlbumDetailView.as_view()),
   path('playlist/<int:pk>/', PlayListDetailView.as_view()),
   
   path('playlists/', PlayListsView.as_view()),
   path('albums/', AlbumsView.as_view()),
   
   path('create_playlist/', PlayListCreateView.as_view()),
   path('delete_playlist/<int:pk>/', PlayListDeleteView.as_view()),
   path('update_playlist/<int:pk>/', PlayListUpdateView.as_view()),

   path('add_song/', AddSongView.as_view()),
   path('remove_song/', RemoveSongView.as_view()),

   path('toggle_song_like/', ToggleSongLikeView.as_view()),
   path('toggle_album_like/', ToggleAlbumLikeView.as_view()),

   # authentication
   path('me/', user),
   path('token/obtain/', TokenObtainPairView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view()),
   path('register/', RegisterView.as_view()),
]