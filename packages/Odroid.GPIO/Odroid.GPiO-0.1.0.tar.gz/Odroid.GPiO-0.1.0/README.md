# Odroid.GPIO

## Installation

```shell
sudo apt update \
&& sudo apt install -y python3 python3-dev python3-pip \
    odroid-wiringpi libwiringpi-dev
```

```bash
python3 -m pip install -U --user pip Odroid.GPIO
```

## Blink example

```python
import Odroid.GPIO as GPIO
# You can also use 'import RPi.GPIO as GPIO'.
import time

'''
GPIO.BCM == GPIO.SOC
GPIO.BOARD
GPIO.WIRINGPI
'''
GPIO.setmode(GPIO.BOARD)

GPIO.setup(35, GPIO.OUT)

while True:
    GPIO.output(35, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(35, GPIO.LOW)
    time.sleep(1)
```

## Changelog

Ref: CHANGELOG
