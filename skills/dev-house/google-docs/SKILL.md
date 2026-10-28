---
name: google-docs
description: "Use when the user wants to create, edit, read, or automate Google Docs. Covers creating documents from templates, inserting text/images/tables, formatting, collaborating, managing comments, converting to PDF, and automating with Google Apps Script. Also use when the user mentions 'Google Doc', 'Google Documents', '.gdoc', 'Docs API', or references a Google Docs URL. Do NOT use for .docx files — use docx instead. Do NOT use for PDFs — use pdf instead."
argument-hint: "[action] [doc_url_or_name] [details]"
metadata:
  category: office-productivity
  tools: google-docs-api, google-apps-script, google-api-python-client
---

# Google Docs Skill

## Triggers
- "Create a Google Doc for..."
- "Edit this Google Doc..."
- "Extract text from Google Docs..."
- "Convert Google Doc to PDF..."
- "Add a table to my Google Doc..."
- "Automate my Google Doc..."
- "Collaborate on Google Docs..."
- "Google Docs API..."

## Capabilities

### 1. Create Document
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

docs = build('docs', 'v1', credentials=creds)

# Create new document
doc = docs.documents().create(body={'title': 'My New Document'}).execute()
doc_id = doc.get('documentId')

# Add text
docs.documents().batchUpdate(
    documentId=doc_id,
    body={
        'requests': [{
            'insertText': {
                'location': {'index': 1},
                'text': 'Hello, World!\n'
            }
        }]
    }
).execute()
```

### 2. Read/Extract Content
```python
# Get full document content
doc = docs.documents().get(documentId=doc_id).execute()
text = doc['body']['content'][0]['paragraph']['elements'][0]['textRun']['content']

# Get all text
def extract_text(doc):
    text = ""
    for block in doc.get('body', {}).get('content', []):
        if 'paragraph' in block:
            for elem in block['paragraph'].get('elements', []):
                if 'textRun' in elem:
                    text += elem['textRun'].get('content', '')
    return text
```

### 3. Add Headings & Formatting
```python
requests = [
    # Add heading
    {
        'insertText': {
            'location': {'index': 1},
            'text': 'Chapter 1: Introduction\n'
        }
    },
    # Format as heading
    {
        'updateParagraphStyle': {
            'range': {'startIndex': 1, 'endIndex': 25},
            'paragraphStyle': {'namedStyleType': 'HEADING_1'},
            'fields': 'namedStyleType'
        }
    },
    # Bold text
    {
        'updateTextStyle': {
            'range': {'startIndex': 30, 'endIndex': 40},
            'textStyle': {'bold': True},
            'fields': 'bold'
        }
    }
]
docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
```

### 4. Insert Tables
```python
requests = [{
    'insertTable': {
        'location': {'index': 100},
        'tableRows': [
            {'tableCells': [
                {'content': [{'paragraph': {'elements': [
                    {'textRun': {'content': 'Header 1'}}
                ]}}],
                 'content': [{'paragraph': {'elements': [
                    {'textRun': {'content': 'Header 2'}}
                ]}}]
            }]
        ]
    }
}]
docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
```

### 5. Insert Images
```python
import base64
with open('chart.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()

requests = [{
    'inlineImage': {
        'uri': f'data:image/png;base64,{img_data}',
        'size': {'magnitude': 200, 'unit': 'PIXELS'}
    }
}]
docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
```

### 6. Collaborate & Share
```python
# Add comment
docs.comments().create(
    documentId=doc_id,
    body={
        'quotedText': 'Some text to comment on',
        'content': 'Please review this section',
        'anchorType': 'QUOTED_TEXT'
    }
).execute()

# Resolve comment
docs.comments().update(
    documentId=doc_id,
    commentId='comment_id',
    body={'resolved': True}
).execute()
```

### 7. Convert to PDF
```python
# Download as PDF via Google Docs API export
import requests
url = f"https://www.googleapis.com/download/docs/v1/documents/{doc_id}/export?format=pdf"
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(url, headers=headers)
with open('document.pdf', 'wb') as f:
    f.write(response.content)
```

### 8. Google Apps Script Automation
```javascript
function onOpen() {
  var ui = DocumentApp.getUi();
  ui.createMenu('Custom Menu')
      .addItem('Generate Report', 'generateReport')
      .addItem('Send to Email', 'sendByEmail')
      .addToUi();
}

function generateReport() {
  var doc = DocumentApp.getActiveDocument();
  var body = doc.getBody();
  body.appendParagraph("Report generated: " + new Date());
}

function sendByEmail() {
  var doc = DocumentApp.getActiveDocument();
  var pdf = doc.getAs(MimeType.PDF);
  MailApp.sendEmail("user@example.com", "Document Report", "See attached.", {attachments: [pdf]});
}
```

## Common Workflows

### Workflow: Automated Report Generation
1. User provides data (from Google Sheets, API, or manual input)
2. Create Google Doc with structured template
3. Insert data sections, tables, and images
4. Format headings, bold/italic as needed
5. Add comments for review
6. Convert to PDF for distribution
7. Optionally email via Apps Script

### Workflow: Document Merging
1. Read multiple Google Docs
2. Extract text/content from each
3. Combine into single master document
4. Apply consistent formatting
5. Save as new Google Doc or export as PDF

### Workflow: Template Filling
1. User has a Google Doc template with placeholders (e.g., `{{NAME}}`, `{{DATE}}`)
2. Parse template, find all `{{VAR}}` patterns
3. Replace with actual values
4. Create new document or update in-place

## MCP Integration
- Google Docs API requires OAuth 2.0 service account
- Scope: `https://www.googleapis.com/auth/documents`
- Combine with `google-sheets` for data-driven reports
- Combine with `pdf` for export workflows
