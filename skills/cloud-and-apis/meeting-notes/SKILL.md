---
name: meeting-notes
description: "Use when the user wants to create, organize, or transcribe meeting notes. Covers meeting agendas, action items tracking, decision logging, participant management, calendar integration, and export to multiple formats. Also use when the user mentions 'meeting notes', 'meeting agenda', 'action items', 'meeting minutes', 'transcribe meeting', or 'meeting summary'. Supports .docx, .pdf, .md, and Google Docs output."
argument-hint: "[meeting_type] [participants] [date]"
metadata:
  category: office-productivity
  tools: python-docx, weasyprint, marked2
---

# Meeting Notes Skill

## Triggers
- "Take meeting notes for..."
- "Create a meeting agenda..."
- "Extract action items from..."
- "Meeting minutes template..."
- "Transcribe this meeting..."
- "Meeting summary..."
- "Follow up on meeting decisions..."

## Meeting Note Structure

### Standard Template
```
MEETING NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Meeting: [Title]
Date: [YYYY-MM-DD]
Time: [Start - End]
Location: [Room/Video Call]
Attendees: [List]
Facilitator: [Name]
Note-taker: [Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AGENDA
1. [Item] — [Owner] — [Time]
2. [Item] — [Owner] — [Time]
3. [Item] — [Owner] — [Time]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ATTENDEES
Present: [Names]
Absent: [Names]
Guests: [Names]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISCUSSION NOTES

[Agenda Item 1]
- [Key point]
- [Decision or outcome]
- [Open questions]

[Agenda Item 2]
- [Key point]
- [Decision or outcome]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISIONS MADE
1. [Decision] — [Rationale] — [Date]
2. [Decision] — [Rationale]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTION ITEMS
| # | Task | Owner | Due Date | Status |
|---|------|-------|----------|--------|
| 1 | [Task] | [Name] | [Date] | Open |
| 2 | [Task] | [Name] | [Date] | Open |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT MEETING
Date: [TBD]
Agenda Preview: [Items]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APPENDIX
[Attachments, references, supporting docs]
```

## Implementation: Meeting Notes Generator

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

class MeetingNotesBuilder:
    def __init__(self, meeting_title):
        self.doc = Document()
        self.meeting_title = meeting_title
        self.action_items = []
        self.decisions = []
        self._setup_styles()
    
    def _setup_styles(self):
        style = self.doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)
    
    def add_header(self, details):
        # Title
        title = self.doc.add_heading(self.meeting_title, level=0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Meta info table
        meta_data = [
            ['Date:', details.get('date', datetime.now().strftime('%Y-%m-%d'))],
            ['Time:', details.get('time', '')],
            ['Location:', details.get('location', '')],
            ['Facilitator:', details.get('facilitator', '')],
            ['Note-taker:', details.get('note_taker', '')],
        ]
        table = self.doc.add_table(rows=len(meta_data), cols=2)
        table.style = 'Table Grid'
        for i, (label, value) in enumerate(meta_data):
            table.rows[i].cells[0].text = label
            table.rows[i].cells[0].width = Inches(1.5)
            table.rows[i].cells[1].text = value
        
        self.doc.add_paragraph()
    
    def add_attendees(self, present, absent=None, guests=None):
        self.doc.add_heading('Attendees', level=1)
        self.doc.add_paragraph(f"Present: {', '.join(present)}")
        if absent:
            self.doc.add_paragraph(f"Absent: {', '.join(absent)}")
        if guests:
            self.doc.add_paragraph(f"Guests: {', '.join(guests)}")
    
    def add_agenda(self, agenda_items):
        self.doc.add_heading('Agenda', level=1)
        for i, item in enumerate(agenda_items, 1):
            p = self.doc.add_paragraph(style='List Number')
            p.add_run(f"{item['topic']}").bold = True
            p.add_run(f" — {item.get('owner', 'TBD')}")
            if item.get('time'):
                p.add_run(f" ({item['time']} min)")
        self.doc.add_paragraph()
    
    def add_discussion(self, items):
        self.doc.add_heading('Discussion Notes', level=1)
        for item in items:
            self.doc.add_heading(f"{item['topic']}", level=2)
            for point in item.get('points', []):
                p = self.doc.add_paragraph(point, style='List Bullet')
                p.paragraph_format.left_indent = Inches(0.5)
            if item.get('decisions'):
                self.doc.add_paragraph("Decisions:")
                for d in item['decisions']:
                    p = self.doc.add_paragraph(d, style='List Bullet')
                    p.paragraph_format.left_indent = Inches(1)
                    self.decisions.append({'topic': item['topic'], 'decision': d})
            if item.get('open_questions'):
                self.doc.add_paragraph("Open Questions:")
                for q in item['open_questions']:
                    p = self.doc.add_paragraph(q, style='List Bullet')
                    p.paragraph_format.left_indent = Inches(1)
    
    def add_action_items(self, items):
        self.doc.add_heading('Action Items', level=1)
        if not items:
            self.doc.add_paragraph("No action items recorded.")
            return
        
        table = self.doc.add_table(rows=1, cols=5)
        table.style = 'Light Grid Accent 1'
        hdr = table.rows[0].cells
        hdr[0].text = '#'
        hdr[1].text = 'Task'
        hdr[2].text = 'Owner'
        hdr[3].text = 'Due Date'
        hdr[4].text = 'Status'
        
        for i, item in enumerate(items, 1):
            row = table.add_row().cells
            row[0].text = str(i)
            row[1].text = item.get('task', '')
            row[2].text = item.get('owner', 'TBD')
            row[3].text = item.get('due_date', 'TBD')
            row[4].text = item.get('status', 'Open')
            self.action_items.append(item)
    
    def add_next_meeting(self, details):
        self.doc.add_heading('Next Meeting', level=1)
        self.doc.add_paragraph(f"Date: {details.get('date', 'TBD')}")
        self.doc.add_paragraph(f"Time: {details.get('time', 'TBD')}")
        self.doc.add_paragraph(f"Agenda Preview: {', '.join(details.get('agenda_preview', []))}")
    
    def add_appendix(self, attachments):
        if not attachments:
            return
        self.doc.add_heading('Appendix', level=1)
        for link in attachments:
            p = self.doc.add_paragraph(link, style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
    
    def save(self, path):
        self.doc.save(path)
        return path
    
    def export_summary(self):
        """Generate a quick summary for email/Slack"""
        summary = f"Meeting: {self.meeting_title}\n\n"
        summary += f"Decisions: {len(self.decisions)}\n"
        for d in self.decisions:
            summary += f"  - {d['topic']}: {d['decision']}\n"
        summary += f"\nAction Items: {len(self.action_items)}\n"
        for item in self.action_items:
            summary += f"  - [{item.get('owner', '?')}] {item.get('task', '?')} (Due: {item.get('due_date', 'TBD')})\n"
        return summary
```

## Common Workflows

### Workflow: Pre-Meeting
1. Create meeting agenda with topics, owners, time allocations
2. Distribute agenda to participants
3. Attach relevant documents/references
4. Set up note-taking template

### Workflow: During Meeting
1. Record discussion points in real-time
2. Flag decisions as they're made
3. Capture action items with owners and due dates
4. Note open questions for follow-up

### Workflow: Post-Meeting
1. Clean up and organize notes
2. Format for readability
3. Distribute to attendees and stakeholders
4. Track action items in project management tool
5. Schedule follow-ups for open questions

### Workflow: Meeting Transcription
1. Receive audio/video file from meeting
2. Transcribe using speech-to-text
3. Structure transcript into discussion sections
4. Extract action items and decisions automatically
5. Generate formatted meeting notes

## Integration with Other Skills
- `google-docs` — create and share notes directly in Google Docs
- `lark-doc` — create notes in Lark/Feishu
- `notion-second-brain` — sync notes to Notion workspace
- `pdf` — export notes as PDF for archival
- `meeting-notes` — reference previous meeting notes for continuity
- `email-templates` — generate distribution emails for meeting notes
