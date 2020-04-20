"""Simulate plant growth and regular capture, for educational purposes; in particular:

- Demonstrating the use of command line argument parsing with click
- Demonstrating writing files to disk in a systematic way

From the command line run 
$ python simulate_timelapse.py --help

Example usage
$ python simulate_timelapse.py --start-recording 2020-01-05T15:32:21 --days=21
"""

import datetime
import ffmpeg
import math
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import click

from constants import CAPTURE_FILE_FORMAT 

logging.basicConfig(level=logging.INFO)
# Plant is growing for one month
START_GROWTH = datetime.datetime(2020, 1, 1)
END_GROWTH = datetime.datetime(2020, 2, 1) - datetime.timedelta(microseconds=1)
GROWTH_LENGTH_S = (END_GROWTH-START_GROWTH).total_seconds()
# Camera is capturing at regular intervals
CAPTURE_INTERVAL = datetime.timedelta(minutes=15)
CAPTURES_PER_DAY = datetime.timedelta(days=1) / CAPTURE_INTERVAL 
# Plant is spiraling with an angular frequency of 1 rad / day. 
OMEGA = math.pi  / CAPTURES_PER_DAY
# Plant growth is simulated in fixed steps (approximation which makes code a bit shorter)
TIME_STEPS = np.arange(0, GROWTH_LENGTH_S, CAPTURE_INTERVAL.total_seconds())
ANGLE_STEPS = OMEGA * np.arange(len(TIME_STEPS)) 
   
def simulate_capture(start_recording: datetime, days=5):
    """Returns pairs of simulated datetime and image

    Simulates timelapse of a sprialing plant.
    Snapshots are taken in regular intervals from 'start_recording'
    The plant grows from 0 to 1 in Janary 2020.


    Args:
        start_recording: First moment of recording. Should in Janary 2020  
        days: Number of days to simulate. start_recording + days should be in January 2020.

    Returns:
        Iterator of tuples of type  (datetime, matplotlib.figure)
    """
    pass


    capture_times = [start_recording + idx * CAPTURE_INTERVAL for idx in range(int(days * CAPTURES_PER_DAY))]
    # Plant is growing in discrete steps of 15 minutes starting at 00:00:00 
    start_idx = math.floor((start_recording - START_GROWTH).total_seconds() / CAPTURE_INTERVAL.total_seconds()) + 1

    for capture_idx, capture_time in enumerate(capture_times): 
        fig = plt.figure(figsize=(12, 12))
        ax = plt.subplot(111, polar=True)
        plt.ylim(0, GROWTH_LENGTH_S)
        ax.get_yaxis().set_visible(False)
        ax.plot(ANGLE_STEPS[:start_idx + capture_idx], TIME_STEPS[:start_idx + capture_idx], linewidth=3, color='green')
        yield capture_time, fig
        plt.close(fig)


@click.command()
@click.option('--start-recording', default=START_GROWTH.strftime('%Y-%m-%d'), type=click.DateTime(), help='First moment of recording. Should in be in Janary 2020')
@click.option('--days', default=10, help='Number of days to record. Last moment of recording must be before February 2020.')
@click.argument('out', type=click.Path(), default='./capture')
def simulate(start_recording: datetime, days=10, out: Path=Path('./capture')):
    """Simulate repeated capture of plant growth.
    Writes captured images to the file system.

    OUT: directory where captures are written. ./capture is used if omitted. 
    """
    for capture_time, fig in simulate_capture(start_recording , days):
        # The next three lines can be used in an analogous way for the Raspbery pi camera capture
        fname  = Path(out) / capture_time.strftime(CAPTURE_FILE_FORMAT)
        os.makedirs(fname.parent, exist_ok=True)
        fig.savefig(fname)
        logging.info('writing capture to {}'.format(fname.as_posix()))


if __name__ == '__main__':
    store_simulated_capture()

