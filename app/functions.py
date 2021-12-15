import mutagen


def format_album_duration(seconds):
   s = seconds % 60
   m = seconds // 60
   h = 0
   if m >= 60:
      h = m // 60
      m = m % 60
   if h > 0:
      if m > 0:
         return f'{h} hr, {m} min'
      return f'{h} hr'
   else:
      if m > 0 and s > 0:
         return f'{m} min, {s} sec'
      elif m > 0:
         return f'{m} min'
      return f'{s} sec'

def format_song_duration(seconds):
   return f'{seconds // 60}:{_add_leading_zero(seconds % 60)}'

def _add_leading_zero(n):
   return f'0{n}' if n < 10 else f'{n}'

def accumulate_songs_duration(songs):
   duration = 0 # time in seconds
   for song in songs:
      audio_info = mutagen.File(song.audio).info
      duration += int(audio_info.length)
   return format_album_duration(duration)