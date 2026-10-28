---
name: google-slides
description: "Use when the user wants to create, edit, read, or automate Google Slides presentations. Covers creating slide decks from scratch, adding text/images/charts, managing layouts, applying themes, converting to PDF/MP4, and automating with Google Apps Script. Also use when the user mentions 'Google Slides', '.gslides', 'Slides API', or references a Google Slides URL. Do NOT use for .pptx files — use pptx instead. Do NOT use for HTML presentations — use slides or frontend-slides instead."
argument-hint: "[action] [deck_url_or_name] [details]"
metadata:
  category: office-productivity
  tools: google-slides-api, google-apps-script, google-presentation-api
---

# Google Slides Skill

## Triggers
- "Create a Google Slides deck for..."
- "Edit this Google Slides presentation..."
- "Add a slide to my Google Slides..."
- "Convert Google Slides to PDF..."
- "Extract text from Google Slides..."
- "Automate Google Slides with Apps Script..."
- "Google Slides API..."

## Capabilities

### 1. Create New Presentation
```python
from googleapiclient.discovery import build

slides = build('slides', 'v1', credentials=creds)

# Create new presentation
presentation = slides.presentations().create(
    body={
        'title': 'My Presentation',
        'slides': [{
            'layoutObjectId': 'MASTER_SLIDE',
            'slideProperties': {'layoutName': 'TITLE_SLIDE'}
        }]
    }
).execute()
presentation_id = presentation.get('presentationId')
```

### 2. Add Slide
```python
slides.presentations().batchUpdate(
    presentationId=presentation_id,
    body={
        'requests': [{
            'createSlide': {
                'objectId': 'slide_2',
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                }
            }
        }]
    }
).execute()
```

### 3. Add Text to Slide
```python
slides.presentations().batchUpdate(
    presentationId=presentation_id,
    body={
        'requests': [{
            'createTextRange': {
                'objectId': 'slide_2',
                'text': 'Hello, World!',
                'style': {
                    'fontSize': {'magnitude': 24, 'unit': 'PT'},
                    'bold': True
                }
            }
        }]
    }
).execute()
```

### 4. Insert Image
```python
import base64
with open('image.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()

slides.presentations().batchUpdate(
    presentationId=presentation_id,
    body={
        'requests': [{
            'createImage': {
                'url': f'data:image/png;base64,{img_data}',
                'elementProperties': {
                    'size': {'width': {'magnitude': 300, 'unit': 'PX'},
                             'height': {'width': {'magnitude': 200, 'unit': 'PX'}},
                    'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 100, 'translateY': 100}
                }
            }
        }]
    }
).execute()
```

### 5. Read/Parse Presentation
```python
presentation = slides.presentations().get(presentationId=presentation_id).execute()

def extract_slides(presentation):
    slides_data = []
    for slide in presentation.get('slides', []):
        slide_data = {'title': '', 'content': []}
        for element in slide.get('pageElements', []):
            if 'shape' in element and 'text' in element['shape']:
                text = element['shape']['text']['textSegments']
                slide_data['content'].extend([t['text']['content'] for t in text])
        slides_data.append(slide_data)
    return slides_data
```

### 6. Apply Theme/Layout
```python
# Get available layouts
presentation = slides.presentations().get(presentationId=presentation_id).execute()
layouts = presentation.get('layouts', [])

# Apply theme via template
# Best practice: Start from a template presentation
template_id = 'your-template-presentation-id'
slides.presentations().copy(
    body={'title': 'Copy with Theme'},
    presentationId=template_id
).execute()
```

### 7. Convert to PDF
```python
import requests
url = f"https://www.googleapis.com/download/docs/v1/presentations/{presentation_id}/export?format=pdf"
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(url, headers=headers)
with open('presentation.pdf', 'wb') as f:
    f.write(response.content)
```

### 8. Google Apps Script Automation
```javascript
function onOpen() {
  var ui = SlidesApp.getUi();
  ui.createMenu('Custom Actions')
      .addItem('Generate Slides from Sheet', 'createFromSheet')
      .addItem('Export as PDF', 'exportPDF')
      .addToUi();
}

function createFromSheet() {
  var deck = SlidesApp.getActivePresentation();
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var data = sheet.getDataRange().getValues();
  
  // Create slides from data
  for (var i = 1; i < data.length; i++) {
    var slide = deck.appendSlide(SlidesApp.PredefinedLayout.TITLE_AND_BODY);
    slide.getTitle().setText(data[i][0]);
    slide.getBody().setText(data[i][1]);
  }
}

function exportPDF() {
  var deck = SlidesApp.getActivePresentation();
  var blob = deck.getAs(MimeType.PDF);
  DriveApp.createFile(blob).setName(deck.getName() + ".pdf");
}
```

### 9. Batch Update Patterns
```python
# Multiple operations in one API call
requests = [
    # Add title slide
    {'createSlide': {'objectId': 'title_slide', 'title': 'Title Slide'}},
    # Add content slide
    {'createSlide': {'objectId': 'content_slide', 'title': 'Content Slide'}},
    # Add text to title
    {'createText': {'objectId': 'title_slide', 'text': 'Project Update'}},
    # Add bullet points
    {'createText': {'objectId': 'content_slide', 'text': '- Q1 Results\n- Q2 Projections\n- Q3 Goals'}},
]
slides.presentations().batchUpdate(
    presentationId=presentation_id,
    body={'requests': requests}
).execute()
```

## Common Workflows

### Workflow: Data-Driven Presentation
1. Read data from Google Sheets or CSV
2. Create new Google Slides deck
3. Generate one slide per data row
4. Apply consistent layout and styling
5. Add charts/images where needed
6. Export as PDF for sharing

### Workflow: Template-Based Deck
1. User provides a Google Slides template
2. Clone template for new deck
3. Replace placeholder text with actual content
4. Insert dynamic charts from Sheets
5. Apply branding/theme consistently

### Workflow: Slide Export Pipeline
1. Read source data (Sheets, API, database)
2. Generate Google Slides deck
3. Convert to PDF for distribution
4. Optionally convert to MP4 (via recording)
5. Email/share with stakeholders

## MCP Integration
- Google Slides API scope: `https://www.googleapis.com/auth/presentations`
- Combine with `google-sheets` for data-driven slides
- Combine with `google-docs` for accompanying documentation
- Combine with `pdf` for export workflows

## Performance Notes
- Batch operations: Always use `batchUpdate` for multiple changes
- Rate limits: 60 requests/minute per project
- Large decks: Consider splitting into multiple presentations
- Templates: Start from existing templates to preserve styling
