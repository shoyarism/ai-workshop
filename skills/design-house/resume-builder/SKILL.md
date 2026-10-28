---
name: resume-builder
description: "Use when the user wants to create, edit, or optimize a resume, CV, or curriculum vitae. Covers ATS-friendly formatting, multiple template styles, content writing for each section, keyword optimization, PDF export, and version comparison. Also use when the user mentions 'resume', 'CV', 'curriculum vitae', 'job application document', 'professional bio', or 'create a resume'. Supports .pdf and .docx output."
argument-hint: "[candidate_name] [target_role] [experience_level]"
metadata:
  category: office-productivity
  tools: python-docx, reportlab, fpdf2, resume-parser
---

# Resume Builder Skill

## Triggers
- "Create a resume for..."
- "Build a CV..."
- "Optimize my resume for..."
- "Resume template..."
- "ATS-friendly resume..."
- "Resume for [role]..."
- "Update my resume..."

## Resume Structure

### Standard Sections
```
[HEADER]
  - Name (large, bold)
  - Title/Role
  - Contact: Email | Phone | LinkedIn | Location

[PROFESSIONAL SUMMARY]
  - 2-4 sentence career overview
  - Key achievements highlighted
  - Tailored to target role

[EXPERIENCE] (reverse chronological)
  - Company, Location | Role | Dates
  - 3-5 bullet points per role
  - Action verb + context + result format
  - Quantify achievements where possible

[EDUCATION]
  - Institution, Location | Degree | Graduation Year
  - Relevant: GPA (if >3.5), honors, relevant coursework

[SKILLS]
  - Technical: Programming languages, frameworks, tools
  - Soft: Leadership, communication, problem-solving
  - Categorize by relevance to target role

[ADDITIONAL SECTIONS] (as relevant)
  - Certifications
  - Projects
  - Publications
  - Languages
  - Volunteering
```

## ATS Optimization Rules
1. **No columns** — ATS parsers struggle with multi-column layouts
2. **Standard fonts** — Arial, Calibri, Georgia, Times New Roman
3. **No tables for layout** — Use simple text structure
4. **Keyword matching** — Mirror language from job description
5. **Standard section headings** — "Experience", "Education", "Skills"
6. **No headers/footers** — Critical info goes in body text
7. **File format** — .docx preferred by many ATS; .pdf second choice
8. **Avoid graphics** — No icons, photos, or text boxes

## Implementation: Resume Generator

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

class ResumeBuilder:
    def __init__(self, name, target_role):
        self.doc = Document()
        self.name = name
        self.target_role = target_role
        self._setup_styles()
    
    def _setup_styles(self):
        style = self.doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)
        
        # Name style
        name_style = self.doc.styles['Heading 1']
        name_style.font.size = Pt(24)
        name_style.font.bold = True
        name_style.font.color.rgb = RGBColor(0, 51, 102)
    
    def add_header(self, contact_info):
        # Name
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(self.name.upper())
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)
        
        # Role
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(self.target_role).font.size = Pt(14)
        
        # Contact
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(contact_info).font.size = Pt(10)
        
        self.doc.add_paragraph()  # spacer
    
    def add_summary(self, text):
        self.doc.add_heading('Professional Summary', level=1)
        p = self.doc.add_paragraph(text)
        p.paragraph_format.first_line_indent = Inches(0.5)
    
    def add_experience(self, experiences):
        self.doc.add_heading('Experience', level=1)
        for exp in experiences:
            # Company line
            p = self.doc.add_paragraph()
            p.add_run(f"{exp['company']} | {exp.get('location', '')}").bold = True
            p.add_run(f" — {exp['role']}").italic = True
            p.add_run(f"  {exp['dates']}")
            
            # Bullet points
            for bullet in exp.get('bullets', []):
                p = self.doc.add_paragraph(bullet, style='List Bullet')
                p.paragraph_format.left_indent = Inches(0.5)
    
    def add_education(self, education):
        self.doc.add_heading('Education', level=1)
        for ed in education:
            p = self.doc.add_paragraph()
            p.add_run(f"{ed['institution']}").bold = True
            p.add_run(f" — {ed['degree']}")
            if ed.get('gpa'):
                p.add_run(f" (GPA: {ed['gpa']})")
            p.add_run(f"  {ed.get('year', '')}")
    
    def add_skills(self, skills):
        self.doc.add_heading('Skills', level=1)
        for category, items in skills.items():
            p = self.doc.add_paragraph()
            p.add_run(f"{category}: ").bold = True
            p.add_run(', '.join(items))
    
    def add_projects(self, projects):
        self.doc.add_heading('Projects', level=1)
        for proj in projects:
            p = self.doc.add_paragraph()
            p.add_run(proj['name']).bold = True
            p.add_run(f" — {proj.get('tech', '')}")
            p = self.doc.add_paragraph(proj.get('description', ''), style='List Bullet')
    
    def save(self, path):
        self.doc.save(path)
        return path
```

## Keyword Optimization Workflow
1. Parse job description for required skills/keywords
2. Compare against candidate's current resume
3. Identify gaps (missing keywords)
4. Suggest additions to experience bullets
5. Recommend skill categorization changes
6. Generate optimized version

## Template Styles

### Modern Clean
- Clean sans-serif fonts
- Subtle accent color for headings
- Generous white space
- Single-column layout

### Classic Professional
- Traditional serif fonts (Georgia, Times)
- Conservative color scheme
- Dense information layout
- Traditional section ordering

### Technical/Engineering
- Monospace font for code-related skills
- Projects section emphasized
- GitHub/portfolio links prominent
- Skills categorized by technology stack

### Executive/C-Suite
- Premium typography
- Achievement-focused summary
- Leadership and impact highlighted
- Board/advisory experience section

## Integration with Other Skills
- `docx` — for final resume document generation
- `pdf` — for PDF export
- `ai-dev-jobs-mcp` — for job-specific keyword optimization
- `email-templates` — for cover letter generation
- `beautiful-article` — for LinkedIn/profile optimization
