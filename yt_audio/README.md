# Instructions

## Dependancies

```bash
pip install pytube
pip install tqdm
```

## Usage

Files will be downloaded to the directory you set in the ```DOWNLOAD_PATH``` variable. 
Playlist's will be saved to a folder inside that download path.
Highest quality streams are the default setting.


**URL / Playlist URL**

```bash
python yt_audio.py -u <url>
```

**URLs from a text file**

```bash
python yt_audio.py -f <path_to_file>
```

**List available audio streams**

```bash
python yt_audio.py -u <url> -s
```

**Download by itag**

```bash
python yt_audio.py -u <url> -t <itag>
```
