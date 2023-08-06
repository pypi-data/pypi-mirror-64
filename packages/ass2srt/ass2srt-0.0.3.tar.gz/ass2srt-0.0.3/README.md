## ass2srt

A tool that convert .ass subtitles to .srt

$ python ass2srt.py -h
```
usage: ass2srt.py [-h] [-s {zh,en,fr,de}] [-l {0,1,2}] [-i] file

positional arguments:
  file                  .ass file to convert

optional arguments:
  -h, --help            show this help message and exit
  -s {zh,en,fr,de}, --suffix {zh,en,fr,de}
                        add suffix to subtitles name
  -l {0,1,2}, --line {0,1,2}
                        keep double subtitles
  -i, --info            display subtitles infomation

```

### Example :
```
python ass2srt.py Movies.S01.E01.Name.ass
```