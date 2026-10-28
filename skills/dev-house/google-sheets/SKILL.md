---
name: google-sheets
description: "Use when the user wants to create, edit, read, or automate Google Sheets. Covers reading/writing cells, creating spreadsheets from scratch, managing sheets and ranges, applying formulas, conditional formatting, charts, sharing permissions, and automating with Google Apps Script. Also use when the user mentions 'Google Sheets', 'gsheets', 'spreadsheet', 'sheets API', or references a Google Sheets URL. Do NOT use for Excel files (.xlsx) — use excel-master or xlsx instead. Do NOT use for raw CSV processing without cloud context — use xlsx for local CSV work."
argument-hint: "[action] [sheet_url_or_name] [details]"
metadata:
  category: office-productivity
  tools: google-sheets-api, google-apps-script, gspread-python
---

# Google Sheets Skill

## Triggers
- "Create a Google Sheet for..."
- "Add data to my Google Sheet..."
- "Read from Google Sheets..."
- "Google Sheets formula..."
- "Automate my Google Sheet..."
- "Share this Google Sheet with..."
- "Create a chart in Google Sheets..."
- "Google Apps Script..."

## Capabilities

### 1. Create New Spreadsheet
```python
# Using gspread (Python)
import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('service_account.json', scopes=scopes)
client = gspread.authorize(creds)

# Create new spreadsheet
sheet = client.create("My New Sheet")
worksheet = sheet.sheet1
worksheet.update('A1', [['Name', 'Score'], ['Alice', 95], ['Bob', 87]])
```

### 2. Read Data
```python
# Open by URL or name
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/...")
worksheet = sheet.sheet1  # or sheet.worksheet("Sheet1")

# Read all data
data = worksheet.get_all_values()        # List of lists
data_dict = worksheet.get_all_records()  # List of dicts (header row)

# Read specific range
cell_range = worksheet.range('A1:C10')
```

### 3. Write/Update Data
```python
# Append rows
worksheet.append_row(["New Item", 42, "Notes"])

# Update range
worksheet.update('B2', [[100], [200]])

# Clear range
worksheet.clear('A1:C10')
```

### 4. Formulas
```python
# Insert formula
worksheet.update('D2', [['=SUM(B2:B10)']])
worksheet.update('E2', [['=AVERAGE(B2:B10)']])
worksheet.update('F2', [['=IF(B2>50,"Pass","Fail")']])
```

### 5. Conditional Formatting
```python
format_rules = [{
    "range": {"startRowIndex": 0, "endRowIndex": 100, "startColumnIndex": 1, "endColumnIndex": 2},
    "conditionalRule": {
        "type": "GREATER_THAN",
        "values": [{"userEnteredValue": "50"}],
        "format": {"backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0}}
    }
}]
worksheet.format({"ranges": ["Sheet1!B2:B101"], "cellFormat": {"backgroundColor": {"red": 1, "green": 0, "blue": 0}}})
```

### 6. Charts
```python
# Via Google Apps Script (run in Sheets UI or via API)
script = '''
function addChart() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var chart = sheet.newChart()
    .asColumnChart()
    .addRange(sheet.getRange('A1:B10'))
    .setPosition(5, 5, 0, 0)
    .build();
  chart.attachTo(sheet);
}
'''
```

### 7. Sharing & Permissions
```python
# Share with email
sheet.share("colleague@example.com", perm_type="user", role="writer")
# Options: perm_type=["user","domain","anyone"], role=["reader","writer","commenter"]
```

### 8. Google Apps Script (Advanced Automation)
```javascript
// Trigger this from Sheets UI: Extensions > Apps Script
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom Actions')
      .addItem('Run Report', 'generateReport')
      .addToUi();
}

function generateReport() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  // Process and create summaries
  var summarySheet = spreadsheet.getSheetByName("Summary");
  if (!summarySheet) summarySheet = spreadsheet.insertSheet("Summary");
  summarySheet.clear().getRange(1,1).setValue("Auto-generated Report");
}
```

## Common Workflows

### Workflow: Create Report from Raw Data
1. User provides raw data (CSV, JSON, or manual input)
2. Create new Google Sheet with structured data
3. Apply formulas for calculations (SUM, AVERAGE, VLOOKUP, Pivot Tables)
4. Add conditional formatting for highlighting
5. Create charts for visualization
6. Set up sharing permissions
7. Optionally automate with Apps Script for recurring updates

### Workflow: Data Pipeline Integration
1. Read data from API/database
2. Write to Google Sheet (append or overwrite)
3. Trigger Apps Script to process/analyze
4. Send notification via email/Slack on completion

## MCP Server: google-workspace
- Available via `@modelcontextprotocol/server-google-workspace` (community)
- Or use Google APIs directly with service account authentication

## Error Handling
- Always handle `gspread.exceptions.SpreadsheetNotFound`
- Rate limit: Google Sheets API has 60 requests/minute per project
- For bulk operations, use `batch_update()` to minimize API calls

## Integration with Other Skills
- `xlsx` — for local spreadsheet work before/after Google Sheets sync
- `docx` — generate reports from sheet data into Word documents
- `pdf` — export sheet ranges as PDF
- `chart-generator` — enhance sheet visualizations
