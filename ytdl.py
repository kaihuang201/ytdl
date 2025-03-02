#!/usr/bin/env python3

# Install pytubefix:
#    pip install pytubefix

from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import argparse
import os
import subprocess
from collections import defaultdict
from pprint import pprint

PROBLEM_CHAR = '?'
DEFAULT_DOWNLOAD_DIR = './static/yt_download'


def combine_av(tmp_path, download_dir=DEFAULT_DOWNLOAD_DIR):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    files = os.listdir(tmp_path)
    file_groups = defaultdict(list)

    # Group files by filename without extension
    for file in files:
        name, ext = os.path.splitext(file)
        file_groups[name].append(file)

    for name, file_list in file_groups.items():
        if len(file_list) == 2:  # Ensure we have exactly two files to merge
            file1, file2 = [os.path.join(tmp_path, f) for f in file_list]
            output_file = os.path.join(download_dir, f"{name}.mp4")

            command = [
                "ffmpeg", "-i", file1, "-i", file2,
                "-c:v", "copy", "-c:a", "aac", "-y", output_file
            ]

            subprocess.run(command, check=True)
            print(f"Merged {file1} and {file2} into {output_file}")

            os.remove(file1)
            os.remove(file2)

def get_best_audio(streams):
    best = None
    for s in streams:
        if s.mime_type.startswith('audio'):
            if not best or int(s.abr[:-4]) > int(best.abr[:-4]):
                best = s
    print(f'Best Audio: {best.abr}')
    return best

def get_best_video(streams):
    best = None
    for s in streams:
        if s.mime_type.startswith('video'):
            if not best or int(best.resolution[:-1]) < int(s.resolution[:-1]):
                best = s
    print(f'Best Video: {best.resolution}')
    return best

def download_video_helper(video_obj, download_dir, audio_only=False, high_res=False):
    if audio_only:
        video_obj.streams.get_audio_only().download(download_dir)
    else:
        streams = video_obj.streams

        if high_res:
            tmp_path = os.path.join(DEFAULT_DOWNLOAD_DIR, "tmp")
            get_best_audio(streams).download(tmp_path)
            get_best_video(streams).download(tmp_path)
            combine_av(tmp_path)
            return

        if streams.get_highest_resolution():
            streams.get_highest_resolution().download(download_dir)
        else:
            streams.first().download(download_dir)

def DownloadPlaylist(pl_url, download_dir, audio_only=False, high_res=False):
    pl = Playlist(pl_url)
    for i, video_obj in enumerate(pl.videos):
        print('Downloading {} / {} in Playlist.'.format(i, len(pl.videos)))
        download_video_helper(video_obj, download_dir, audio_only, high_res)

def DownloadVideo(vid_url, download_dir, audio_only=False, high_res=False):
    video_obj = YouTube(vid_url, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)
    download_video_helper(video_obj, download_dir, audio_only, high_res)

def DownloadURLs(vid_or_playlist_urls, download_dir, audio_only, high_res):
    for url in vid_or_playlist_urls:
        if 'youtube.com/playlist?list=' in url:
            DownloadPlaylist(url, download_dir, audio_only, high_res)
        else:
            DownloadVideo(url, download_dir, audio_only, high_res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--audio_only', help='Will download audio only if specified.', action=argparse.BooleanOptionalAction)
    parser.add_argument('-r', '--high_res', help='Will download highest resolution if specified.', action=argparse.BooleanOptionalAction)
    parser.add_argument('urls', nargs='*')
    parser.add_argument('-d', '--download_dir', help='Directory to save the download files.', default=DEFAULT_DOWNLOAD_DIR)
    args = parser.parse_args()

    print('URLs =', args.urls)
    print('Audio Only =', args.audio_only)
    print('High res =', args.high_res)
    print('Download Dir =', args.download_dir)
    DownloadURLs(args.urls, args.download_dir, args.audio_only, args.high_res);
