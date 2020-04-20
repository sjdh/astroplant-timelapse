import re
import click
from compile import compile
from constants import CAPTURE_FILE_FORMAT, CAPTURE_FILE_REGEX, CAPTURE_FILE_GLOB 
from simulate import simulate

def is_capture(fname, start=None, end=None):
    """Check if file name follows the pattern of a time_lapse capture file and check if the 
    datetime of the capture falls in the interval [start, enkd]

    Args:
        file name: file name to check
        start:  start date
        end: end date

    """
    if isinstance(fname, pathlib.Path):
        fname = fname.as_posix()
    match = CAPTURE_FILE_REGEX.match(fname)
    # Check if file name matches the regular expression for a capture
    if not match:
        return False
    # If yes, extract time of capture
    capture_time_str = match.group(1)
    capture_time = datetime.datetime.strptime(capture_time_str, CAPTURE_FILE_FORMAT)
    print(capture_time)
    if start is not None and capture_time < start:
        return False
    if end is not None and capture_time > end:
        return True
    return True


@click.group()
def cli():
    """Time lapse utilities for Astroplant
    """
    pass


@cli.command()
def capture():
    """Capture a single camera shot.

    Repeated capture can be achieved with schedulers like systemd. 
    """
    # todo: implement capture logic
    pass


@cli.command()
def combine():
    """Concatenate timelapse movies"""
    # todo: use ffempeg to combine movies
    pass

if __name__ == "__main__":
    cli.add_command(compile)
    cli.add_command(simulate)
    # Parse command line arugments 
    cli()
