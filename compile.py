"""Compile movie from timelapse"""
import pathlib
from pathlib import Path
import datetime
import click
from constants import CAPTURE_FILE_FORMAT, CAPTURE_FILE_REGEX, CAPTURE_FILE_GLOB 
import re
import cv2
from tqdm import tqdm

@click.command()
@click.option('--start', default=None, type=click.DateTime(), help='Ignore captures taken before this moment.')
@click.option('--end', default=None, type=click.DateTime(), help='Ignore captures taken after this moment.')
@click.option('--path', type=click.Path(), default=Path('./capture'), help='directory where captured images are stored. ./capture is used if omitted.')
@click.option('--out', type=click.Path(), default=Path('./'), )
def compile(path, out, start, end):
    """
    Compile movie from time lapse images.

    Example of expected directory structure:
        capture
        ├── 2020-01-05
        │   ├── capture_15:32:21.png
        │   ├── capture_15:47:21.png
        │   ├── capture_16:02:21.png
        │   ...
        ├── 2020-01-06
        │   ├── capture_00:02:21.png
        │   ├── capture_00:17:21.png
        │   ├── capture_00:32:21.png
        │   ...
        ...
    """
    frame_rate = 30
    glob = path.glob(CAPTURE_FILE_GLOB)
    fnames = sorted(glob)
    height, width, _ = cv2.imread(fnames[0].as_posix()).shape
    video_name = 'timelapse_{begin}-{end}.avi'.format(begin=fnames[0].parent.name, end=fnames[2].parent.name)
    video_path = out / video_name
    height, width, _  = cv2.imread(fnames[0].as_posix()).shape
    fourcc = cv2.VideoWriter_fourcc(*'FMP4')
    video = cv2.VideoWriter(video_path.as_posix(), fourcc, frame_rate, (width, height))
    print("Writing timlapse movie to {}".format(video_name))
    for fname in tqdm(fnames, desc="writing frames"):
        frame = cv2.imread(fname.as_posix())
        video.write(frame)
    video.release()

if __name__ == "__main__":
    compile_movie()

