import os
import pandas as pd
import sys
import json5
import spotipy
import spotipy.util as util
import seaborn as sns
import matplotlib.pyplot as plt
usuario = sys.argv[1]

try:
    token = util.prompt_for_user_token(usuario)
except:
    os.remove(f'.cache-{usuario}')
    token = util.prompt_for_user_token(usuario)
sp = spotipy.Spotify(auth=token)
playlists = sp.current_user_playlists()
playlists = playlists['items']
nombres = []
num_canciones = []
id = []
for i in playlists:
    for key in i.keys():
        if key == 'name':
            nombres.append(i.get('name'))
        elif key == 'tracks':
            num_canciones.append(i.get('tracks'))
        elif key == 'id':
            id.append(i.get('id'))
canciones = []
#for i in num_canciones:
    #i.pop('href')
    #canciones.append(i.get('total'))
#mis_playlists = pd.DataFrame({'id':id,'nombres':nombres,'num_canciones':canciones })

artista_id = []
for i in range(len(id)):
    piloto = sp.playlist_tracks(id[i], limit=100)

    for i in piloto['items']:
        artista_id.append(i['track']['artists'][0]['id'])

artista_genero = []
for i in range(len(artista_id)):
    temp = sp.artist(artist_id=artista_id[i])
    for x in temp['genres']:
        artista_genero.append(x)
tus_top_generos = pd.Series(artista_genero).value_counts()
top_generos = tus_top_generos.sort_values(ascending=False).head(20)
top_generos = top_generos.reset_index(name='num')
ax = sns.barplot(data = top_generos,x ='index', y = 'num')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set(xlabel='Tus Generos Mas Escuchados', ylabel = 'Numero de Canciones en tus Playlists')
plt.show()