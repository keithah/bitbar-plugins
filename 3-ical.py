#!/usr/local/bin/python3

# <bitbar.title>iCalBuddy Display</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Finn Le Sueur</bitbar.author>
# <bitbar.author.github>finnito</bitbar.author.github>
# <bitbar.desc>Displays upcoming events in the menu bar using the iCalBuddy CLI.</bitbar.desc>
# <bitbar.dependencies>python, icalbuddy</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/Finnito/bitbar-plugins</bitbar.abouturl>


import subprocess

process = subprocess.Popen(['/usr/local/bin/icalbuddy --excludeCalTypes --excludeAllDayEvents --includeOnlyEventsFromNowOn --noCalendarNames --timeFormat "%H:%M" eventsToday'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     shell=True)

stdout, stderr = process.communicate()
events = stdout.decode('utf-8')
events = events.split("• ")
events = events[1:]

parsedEvents = []

for i, rawEvent in enumerate(events):
    event = {}
    eventArray = rawEvent.split("\n")[:-1]

    # Title
    event["title"] = eventArray[0]

    # Location
    for attribute in eventArray:
        attribute = attribute.strip()
        if attribute.startswith("location"):
            event["location"] = attribute.split(": ")[1]

    # Time
    event["time"] = eventArray[-1].strip()

    parsedEvents.append(event)


output = "📆 "

if len(parsedEvents) == 0:
    output += "No More Events! 🙌"

for i, event in enumerate(parsedEvents):
    if "location" in event:
        output += f"[{event['time']}] {event['title']} @ {event['location']}\n"
    else:
        output += f"[{event['time']}] {event['title']}\n"
    if i == 0:
        output += "---\n"

print(output)