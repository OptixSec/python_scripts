# Audio Converter

Simple tool I use to convert my music library with.

## Instructions

### Dependencies

Make sure ```Python``` and ```ffmpeg``` are installed on your system.

Install the ```ffmpeg```Python package.

```bash
pip install ffmpeg-python
```

### Usage

Converted files are output in the same folder as the input files.
The default directory it checks for input files is ```~/Music/youtube_downloads```.
By default the input file is kept in place, pass the ```-r``` flag to remove all the input files.

**Convert all**

```bash
python audio_converter
```

**Convert from specified directory**

```bash
python audio_converter -d <dir>
```

**Convert and remove source files**

```bash
python audio_converter -r
```

or

```bash
python audio_converter -d <dir> -r
```