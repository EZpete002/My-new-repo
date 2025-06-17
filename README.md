# Shift Alarm Script

This repository contains a simple Python script `shift_alarm.py` that scans a calendar file for shift start times and schedules alarms on your Alexa device two hours before each shift.

## Requirements

- Python 3
- `requests` and `ics` packages (install via `pip install requests ics`)
- An Alexa access token with permission to create reminders (`alexa::alerts:reminders:skill:readwrite` scope)
- An ICS calendar file containing your work shifts (events should include the word "Shift" in the title by default)

## Usage

```bash
python shift_alarm.py path/to/calendar.ics <ACCESS_TOKEN> <TIMEZONE>
```

Example timezone format: `America/New_York`.

You can change the keyword used to detect shift events with `--keyword`.

The script sends a POST request to `https://api.amazonalexa.com/v1/alerts/reminders` for each upcoming shift and sets a reminder two hours before the start time.
