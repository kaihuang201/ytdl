# ytdl.py
Simple command line tool using pytubefix for YouTube videos downloading.

```
$ ./ytdl.py -h
usage: ytdl.py [-h] [-a | --audio_only | --no-audio_only] [-d DOWNLOAD_DIR] [urls ...]

positional arguments:
  urls

options:
  -h, --help            show this help message and exit
  -a, --audio_only, --no-audio_only
                        Will download audio only and save as mp3 if specified.
  -d DOWNLOAD_DIR, --download_dir DOWNLOAD_DIR
                        Directory to save the download files.
```

# ytserver.py
Simple web server that provides a webpage for downloading.

```
usage: ydserver.py [-h] [ip] [port]

positional arguments:
  ip
  port

options:
  -h, --help  show this help message and exit
```

`python3 ytserver.py <IP> <PORT>`

IP & port can be omitted:
`python3 ytserver.py`

Which is equivalent to using the default values:
`python3 ytserver.py 0.0.0.0 10000`
