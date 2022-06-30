import requests
import re
from bs4 import BeautifulSoup
from enum import Enum
from config import config

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


try:
    sp_api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET))
    api = True
except:
    api = False


def clean_sclink(track):
    if track.startswith("https://m."):
        track = track.replace("https://m.", "https://")
    if track.startswith("http://m."):
        track = track.replace("http://m.", "https://")
    return track


def convert_spotify(url):
    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.search(regex, url):
        result = regex.search(url)
        url = result.group(0)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('title')
    title = title.string
    title = title.replace(', a song by', '').replace(' on Spotify', '')

    return title


def get_spotify_playlist(url):
    """Return Spotify_Playlist class"""

    code = url.split('/')[4].split('?')[0]

    if api == True:

        if "open.spotify.com/album" in url:
            try:
                results = sp_api.album_tracks(code)
                tracks = results['items']

                while results['next']:
                    results = sp_api.next(results)
                    tracks.extend(results['items'])

                links = []

                for track in tracks:
                    try:
                        links.append(track['external_urls']['spotify'])
                    except:
                        pass
                return links
            except:
                if config.SPOTIFY_ID != "" or config.SPOTIFY_SECRET != "":
                    print("ERROR: Check spotify CLIENT_ID and SECRET")

        if "open.spotify.com/playlist" in url:
            try:
                results = sp_api.playlist_items(code)
                tracks = results['items']
                while results['next']:
                    results = sp_api.next(results)
                    tracks.extend(results['items'])

                links = []

                for track in tracks:
                    try:
                        links.append(
                            track['track']['external_urls']['spotify'])
                    except:
                        pass
                return links

            except:
                if config.SPOTIFY_ID != "" or config.SPOTIFY_SECRET != "":
                    print("ERROR: Check spotify CLIENT_ID and SECRET")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all(property="music:song", attrs={"content": True})

    links = []

    for item in results:
        links.append(item['content'])

    title = soup.find('title')
    title = title.string

    return links


def get_url(content):

    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.search(regex, content):
        result = regex.search(content)
        url = result.group(0)
        return url
    else:
        return None


class Sites(Enum):
    Spotify = "Spotify"
    Spotify_Playlist = "Spotify Playlist"
    YouTube = "YouTube"
    Twitter = "Twitter"
    SoundCloud = "SoundCloud"
    Bandcamp = "Bandcamp"
    Custom = "Custom"
    Unknown = "Unknown"


class Playlist_Types(Enum):
    Spotify_Playlist = "Spotify Playlist"
    YouTube_Playlist = "YouTube Playlist"
    BandCamp_Playlist = "BandCamp Playlist"
    Unknown = "Unknown"


class Origins(Enum):
    Default = "Default"
    Playlist = "Playlist"


def identify_url(url):
    if url is None:
        return Sites.Unknown

    if "https://www.youtu" in url or "https://youtu.be" in url:
        return Sites.YouTube

    if "https://open.spotify.com/track" in url:
        return Sites.Spotify

    if "https://open.spotify.com/playlist"in url or "https://open.spotify.com/album" in url:
        return Sites.Spotify_Playlist

    if "bandcamp.com/track/" in url:
        return Sites.Bandcamp

    if "https://twitter.com/" in url:
        return Sites.Twitter

    if url.lower().endswith(config.SUPPORTED_EXTENSIONS):
        return Sites.Custom

    if "soundcloud.com/" in url:
        return Sites.SoundCloud

    # If no match
    return Sites.Unknown


def identify_playlist(url):
    if url is None:
        return Sites.Unknown

    if "playlist?list=" in url:
        return Playlist_Types.YouTube_Playlist

    if "https://open.spotify.com/playlist"in url or "https://open.spotify.com/album" in url:
        return Playlist_Types.Spotify_Playlist

    if "bandcamp.com/album/" in url:
        return Playlist_Types.BandCamp_Playlist

    return Playlist_Types.Unknown
