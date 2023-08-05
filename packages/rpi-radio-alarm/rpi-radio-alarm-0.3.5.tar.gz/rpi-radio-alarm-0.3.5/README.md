# rpi-radio-alarm
Package to simplify the communication to a instance of the [rpi-radio-alarm](https://github.com/bb4L/rpi-radio-alarm)

# Usage
`pip install rpi-radio-alarm`

## Objects
This package includes two classes.

### ApiHelper
This class can handle commands and arguments and send them to the [rpi-radio-alarm](https://github.com/bb4L/rpi-radio-alarm) and return the response

This is done in the `do_command(cmd, args)`, `cmd` has to be one of `constants.COMMANDS` and `args` is a dictionary with the appropiate values.

### RpiArgumentParser
The `RpiArgumentParser` parses string input to correct arguments for the ApiHelper.

### ResponseParser
This class defines for the `ApiHelper` how to parse the response from the [rpi-radio-alarm](https://github.com/bb4L/rpi-radio-alarm).

# Example Usages
[rpi-radio-alarm-discordbot-python](https://github.com/bb4L/rpi-radio-alarm-discordbot-python)

[rpi-radio-alarm-telegrambot](https://github.com/bb4L/rpi-radio-alarm-telegrambot/)

# License
[LGPLv3](LICENSE)