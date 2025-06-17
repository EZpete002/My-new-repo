import argparse
import json
import requests
from ics import Calendar
from datetime import timedelta


def parse_calendar(path):
    with open(path, 'r') as f:
        c = Calendar(f.read())
    return c.events


def filter_shift_events(events, keyword="shift"):
    keyword = keyword.lower()
    return [e for e in events if e.name and keyword in e.name.lower()]


def create_reminder(start_time, token, timezone, message="Upcoming shift"):
    scheduled_time = (start_time - timedelta(hours=2)).format('YYYY-MM-DDTHH:mm:ss')
    url = "https://api.amazonalexa.com/v1/alerts/reminders"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "trigger": {
            "type": "SCHEDULED_ABSOLUTE",
            "scheduledTime": scheduled_time,
            "timeZoneId": timezone
        },
        "alertInfo": {
            "spokenInfo": {
                "content": [{
                    "locale": "en-US",
                    "text": message
                }]
            }
        },
        "pushNotification": {"status": "ENABLED"}
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code != 201:
        print("Failed to set reminder:", response.status_code, response.text)
    else:
        print("Reminder set for", scheduled_time)


def main():
    parser = argparse.ArgumentParser(description="Set Alexa reminders for shifts")
    parser.add_argument("ics", help="Path to calendar ICS file")
    parser.add_argument("token", help="Alexa access token")
    parser.add_argument("timezone", help="Timezone id, e.g. America/New_York")
    parser.add_argument("--keyword", default="shift", help="Event name keyword")
    args = parser.parse_args()

    events = parse_calendar(args.ics)
    shifts = filter_shift_events(events, args.keyword)
    for ev in shifts:
        create_reminder(ev.begin, args.token, args.timezone,
                        message=f"Shift at {ev.begin.format('YYYY-MM-DD HH:mm')}")


if __name__ == "__main__":
    main()
