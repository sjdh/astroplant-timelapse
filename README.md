# Timelapse for Astroplant
This is a timelapse tool for the astroplant project. 
To be used with atroplant setup, based on Raspberry Pi.




## Usage

Show help
```bash
python timelapse.py --help
python timelapse.py capture --help
python timelapse.py simulate --help
```

Simulate 
```bash

# Write repeated simulated capture to ./capture 
python timelapse.py simulate --start-recording 2020-01-05T15:32:21 --days=20 ./capture
```


## Directory structure


`timelapse` stores and reads captures in the following directory structure

```
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
```

## Capture periodically
`timelapse` does not implement a schedular.
Hoever, systemd is an excelent choise as a schedular and it is present on most linux systems.

To schedule a priodic capture, first create a new service. 

```ini
# /etc/systemd/system/timlapse-capture.service
[Unit]
Description=Captures a single timelapse shot

[Service]
Type=oneshot
ExecStart=/usr/bin/python /home/ubuntu/atro-timelapse/timelapse capture
WorkingDirectory=/home/ubuntu/timelapse
```
Adapt to your specifics and then create a timer file

```ini
# /etc/systemd/system/timlapse-capture.timer

[Unit]
Description=Run timelapse capture every 15 minutes

[Timer]
OnStartupSec=15min

[Install]
WantedBy=timers.target
```

List timers
```bash
systemctl list-timers
```

Enble timer on boot
```bash
systemctl enable timelapse-capture.timer
```

Start timer
```bash
systemctl start timelapse-capture.timer
```

## Requirements

Python3

**to do:** add requirements.txt