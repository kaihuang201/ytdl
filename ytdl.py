#!/usr/bin/env python3

# Install pytubefix:
#    pip install pytubefix

from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import argparse

PROBLEM_CHAR = '?'
DEFAULT_DOWNLOAD_DIR = 'yt_download'

def download_video_helper(video_obj, download_dir, audio_only=False):
    if audio_only:
        video_obj.streams.get_audio_only().download(download_dir)
    else:
        streams = video_obj.streams
        #print("STREAMS::")
        #print(streams)
        if streams.get_highest_resolution():
            streams.get_highest_resolution().download(download_dir)
        else:
            streams.first().download(download_dir)

def DownloadPlaylist(pl_url, download_dir, audio_only=False):
    pl = Playlist(pl_url)
    for i, video_obj in enumerate(pl.videos):
        print('Downloading {} / {} in Playlist.'.format(i, len(pl.videos)))
        download_video_helper(video_obj, download_dir, audio_only)

def DownloadVideo(vid_url, download_dir, audio_only=False):
    video_obj = YouTube(vid_url, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)
    download_video_helper(video_obj, download_dir, audio_only)

def DownloadURLs(vid_or_playlist_urls, download_dir, audio_only):
    for url in vid_or_playlist_urls:
        if 'youtube.com/playlist?list=' in url:
            DownloadPlaylist(url, download_dir, audio_only)
        else:
            DownloadVideo(url, download_dir, audio_only)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--audio_only', help='Will download audio only and save as mp3 if specified.', action=argparse.BooleanOptionalAction)
    parser.add_argument('urls', nargs='*')
    parser.add_argument('-d', '--download_dir', help='Directory to save the download files.', default=DEFAULT_DOWNLOAD_DIR)
    args = parser.parse_args()

    print('URLs =', args.urls)
    print('Audio Only =', args.audio_only)
    print('Download Dir =', args.download_dir)
    DownloadURLs(args.urls, args.download_dir, args.audio_only);
