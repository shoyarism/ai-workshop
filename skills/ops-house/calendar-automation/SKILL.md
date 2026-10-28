---
name: calendar-automation
description: "Use when the user wants to create, manage, or automate calendar events and scheduling. Covers event creation, meeting scheduling, availability checking, timezone handling, recurring events, calendar sync, and automated reminders. Also use when the user mentions 'calendar', 'schedule', 'meeting', 'appointment', 'availability', 'booking', 'time zone', or 'calendar integration'. Supports Google Calendar, Outlook/365, and iCal formats."
argument-hint: "[action] [event_details]"
metadata:
  category: office-productivity
  tools: google-calendar-api, icalendar, python-dateutil
---

# Calendar Automation Skill

## Triggers
- "Create a calendar event for..."
- "Schedule a meeting..."
- "Check availability for..."
- "Add recurring events..."
- "Calendar sync..."
- "Time zone converter..."
- "Set up reminders..."
- "Booking link..."

## Calendar API Patterns

### Google Calendar (Python)
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pytz

def create_event(service, event_data):
    """Create a calendar event"""
    event = {
        'summary': event_data.get('summary', 'Meeting'),
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': event_data['start'].isoformat(),
            'timeZone': event_data.get('time_zone', 'UTC')
        },
        'end': {
            'dateTime': event_data['end'].isoformat(),
            'timeZone': event_data.get('time_zone', 'UTC')
        },
        'location': event_data.get('location', ''),
        'attendees': event_data.get('attendees', []),
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': event_data.get('email_reminder', 24 * 60)},
                {'method': 'popup', 'minutes': event_data.get('popup_reminder', 10)},
            ]
        },
        'conferenceData': event_data.get('conference', {}),
    }
    
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()
    return event

def check_availability(service, calendar_id, time_min, time_max, attendees=None):
    """Check free/busy times"""
    body = {
        'timeMin': time_min.isoformat(),
        'timeMax': time_max.isoformat(),
        'items': [{'id': calendar_id}]
    }
    if attendees:
        body['attendees'] = [{'email': email} for email in attendees]
    
    return service.freebusy().query(body=body).execute()

def find_available_slots(service, duration_minutes=60, working_hours=None, 
                        days_ahead=7, exclude_calendars=None):
    """Find available time slots for a meeting"""
    now = datetime.now(pytz.UTC)
    end = now + timedelta(days=days_ahead)
    
    # Get all calendars
    calendars = service.calendars().list().execute()
    
    # For each day, check working hours
    slots = []
    current = now.replace(hour=9, minute=0, second=0, microsecond=0)
    
    while current < end:
        day_end = current.replace(hour=18, minute=0, second=0, microsecond=0)
        
        # Check if working day (Mon-Fri)
        if current.weekday() < 5:
            # Query busy times
            time_min = current.isoformat()
            time_max = day_end.isoformat()
            
            busy_response = service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            # Find free slots
            busy = sorted([
                (event['start'].get('dateTime', event['start'].get('date')),
                 event['end'].get('dateTime', event['end'].get('date')))
                for event in busy_response.get('items', [])
            ])
            
            # Calculate free slots
            free_slots = calculate_free_slots(current, day_end, busy, duration_minutes)
            slots.extend(free_slots)
        
        current += timedelta(days=1)
    
    return slots

def calculate_free_slots(day_start, day_end, busy_times, duration):
    """Calculate free time slots in a day"""
    free_slots = []
    current = day_start
    
    for start, end in busy_times:
        start = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end.replace('Z', '+00:00'))
        
        if current < start and (start - current) >= timedelta(minutes=duration):
            free_slots.append({
                'start': current,
                'end': current + timedelta(minutes=duration),
                'duration_minutes': duration
            })
        
        current = max(current, end)
    
    # Check remaining time
    if current < day_end and (day_end - current) >= timedelta(minutes=duration):
        free_slots.append({
            'start': current,
            'end': current + timedelta(minutes=duration),
            'duration_minutes': duration
        })
    
    return free_slots
```

### iCal Format (for cross-platform compatibility)
```python
from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta

def create_ical_event(summary, start, end, description='', location='', 
                      attendees=None, alarm_minutes=10):
    """Create an iCal event"""
    cal = Calendar()
    cal.add('prodid', '-//Workshop Calendar//')
    cal.add('version', '2.0')
    
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('dtstamp', datetime.now())
    
    if description:
        event.add('description', description)
    if location:
        event.add('location', location)
    if attendees:
        for attendee in attendees:
            event.add('attendee', f'MAILTO:{attendee}')
    
    # Add alarm
    alarm = Event()
    alarm.add('summary', 'Reminder')
    alarm.add('action', 'DISPLAY')
    alarm.add('trigger', timedelta(minutes=-alarm_minutes))
    event.add_component(alarm)
    
    cal.add_component(event)
    return cal.to_ical()
```

## Common Calendar Workflows

### Workflow: Meeting Scheduling
1. User provides meeting details (topic, duration, attendees)
2. Check availability of all attendees
3. Find mutually convenient time slot
4. Create calendar event with details
5. Send invites to attendees
6. Set up reminders
7. Optionally create video conference link

### Workflow: Recurring Events
1. Define recurrence pattern (daily, weekly, monthly)
2. Set end date or number of occurrences
3. Create recurring event
4. Handle exceptions (holidays, special cases)
5. Sync across time zones

### Workflow: Availability Calendar
1. Collect team member calendars
2. Find common free time
3. Display as booking links
4. Handle timezone differences
5. Prevent double-booking

### Workflow: Time Zone Converter
1. Convert event times between time zones
2. Handle DST transitions
3. Display in attendee's local time
4. Send correct times in invitations

## Template: Meeting Invitation
```python
def create_meeting_invite(event_data):
    """Create a complete meeting invitation"""
    return {
        'summary': event_data.get('summary', 'Meeting'),
        'start': event_data['start_time'],
        'end': event_data['end_time'],
        'timezone': event_data.get('timezone', 'UTC'),
        'location': event_data.get('location', 'Video Call'),
        'description': event_data.get('description', ''),
        'agenda': event_data.get('agenda', []),
        'attendees': event_data.get('attendees', []),
        'conference': event_data.get('conference_link', ''),
        'reminders': {
            'email': event_data.get('email_reminder', 24),  # hours before
            'popup': event_data.get('popup_reminder', 10)   # minutes before
        },
        'resources': event_data.get('resources', [])
    }
```

## Integration Points

### Google Calendar API
- Scope: `https://www.googleapis.com/auth/calendar`
- Rate limit: 1,000,000 requests per day
- Key endpoints: events.insert, events.list, events.update

### Outlook/Office 365
- Scope: `Calendars.ReadWrite`
- Use Microsoft Graph API
- Key endpoints: /me/events, /calendars/{id}/events

### iCal/Exchange
- Standard format for cross-platform sync
- Use icalendar Python library
- Good for email attachments and webcal feeds

## Best Practices
1. Always handle time zones explicitly
2. Set reminders for all events
3. Include video conference links
4. Send calendar invites, not just email
5. Handle cancellations and updates
6. Respect Do Not Disturb settings
7. Use recurrence patterns for regular meetings
8. Provide cancellation/refund policies for external bookings

## Integration with Other Skills
- `meeting-notes` — create events from meeting templates
- `email-templates` — send calendar invites via email
- `lark-calendar` — for Lark/Feishu calendar integration
- `notion-second-brain` — sync events to Notion
- `calendar-automation` — for advanced scheduling logic
