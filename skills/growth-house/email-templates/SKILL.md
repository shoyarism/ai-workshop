---
name: email-templates
description: "Use when the user wants to create, customize, or automate email templates. Covers professional email templates, newsletter layouts, transactional emails, cold outreach, follow-up sequences, and email campaign design. Also use when the user mentions 'email template', 'email copy', 'newsletter', 'drip campaign', 'cold email', 'follow-up email', 'transactional email', or 'email sequence'. Supports plain text, HTML, and markdown formats."
argument-hint: "[email_type] [context] [tone]"
metadata:
  category: office-productivity
  tools: jinja2, markdown, html-email, sendgrid-templates
---

# Email Templates Skill

## Triggers
- "Create an email template for..."
- "Write a cold email to..."
- "Generate a follow-up email..."
- "Email sequence for..."
- "Newsletter template..."
- "Transactional email template..."
- "Welcome email..."
- "Abandoned cart email..."

## Email Template Categories

### Transactional
| Type | Subject Line Pattern | Key Elements |
|------|---------------------|--------------|
| Welcome | "Welcome to [Product]!" | Greeting, next steps, CTA |
| Password Reset | "Reset your password" | Link, expiry, security tip |
| Order Confirmation | "Order #[ID] confirmed" | Order details, tracking, support |
| Shipping Update | "Your order is on the way" | Tracking, ETA, support |
| Payment Receipt | "Payment received - $[Amount]" | Amount, date, receipt link |

### Marketing
| Type | Subject Line Pattern | Key Elements |
|------|---------------------|--------------|
| Newsletter | "[Topic] - This Week's Update" | Headline, 3-5 items, CTA |
| Promotional | "Exclusive: [Offer]" | Urgency, benefit, CTA |
| Re-engagement | "We miss you - [Offer]" | Acknowledgment, incentive, CTA |
| Product Launch | "Introducing [Product]" | Announcement, features, CTA |

### Sales/Outreach
| Type | Subject Line Pattern | Key Elements |
|------|---------------------|--------------|
| Cold Outreach | "Question about [Company]" | Personalization, value prop, CTA |
| Follow-up | "Following up on [Topic]" | Reference, reminder, CTA |
| Meeting Request | "Meeting request - [Name]" | Context, time proposal, CTA |
| Proposal | "Proposal: [Project Name]" | Summary, value, next steps |

## Implementation: Email Template System

```python
from jinja2 import Template
from datetime import datetime
import markdown

class EmailTemplateEngine:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        return {
            'welcome': {
                'subject': 'Welcome to {{company}}! Here\'s how to get started',
                'preview_text': 'Your account is ready. Complete these 3 quick steps.',
                'html': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to {{company}}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8f9fa;">
    <table role="presentation" style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <tr>
            <td style="padding: 40px 40px 20px; text-align: center; background-color: {{primary_color}};">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Welcome to {{company}}!</h1>
            </td>
        </tr>
        
        <!-- Content -->
        <tr>
            <td style="padding: 40px;">
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Hi {{first_name}},
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Thanks for joining {{company}}! We're excited to have you on board.
                    Here's how to get started in 3 quick steps:
                </p>
                
                <!-- Steps -->
                <table style="width: 100%; margin: 30px 0;">
                    <tr>
                        <td style="padding: 15px; background-color: #f0f7ff; border-radius: 8px; text-align: center;">
                            <span style="display: block; font-size: 24px; font-weight: bold; color: {{primary_color}};">1</span>
                            <span style="color: #333333;">Complete your profile</span>
                        </td>
                        <td style="padding: 15px; background-color: #f0f7ff; border-radius: 8px; text-align: center;">
                            <span style="display: block; font-size: 24px; font-weight: bold; color: {{primary_color}};">2</span>
                            <span style="color: #333333;">Explore features</span>
                        </td>
                        <td style="padding: 15px; background-color: #f0f7ff; border-radius: 8px; text-align: center;">
                            <span style="display: block; font-size: 24px; font-weight: bold; color: {{primary_color}};">3</span>
                            <span style="color: #333333;">Start creating</span>
                        </td>
                    </tr>
                </table>
                
                <!-- CTA -->
                <table style="width: 100%; text-align: center; margin: 30px 0;">
                    <tr>
                        <td>
                            <a href="{{get_started_url}}" 
                               style="background-color: {{primary_color}}; color: #ffffff; 
                                      padding: 14px 32px; text-decoration: none; 
                                      border-radius: 6px; font-weight: 600; 
                                      display: inline-block;">
                                Get Started Now
                            </a>
                        </td>
                    </tr>
                </table>
                
                <p style="font-size: 14px; color: #666666; line-height: 1.6;">
                    Need help? Reply to this email or visit our 
                    <a href="{{help_url}}" style="color: {{primary_color}};">help center</a>.
                </p>
            </td>
        </tr>
        
        <!-- Footer -->
        <tr>
            <td style="padding: 20px 40px; text-align: center; background-color: #f8f9fa; 
                       border-top: 1px solid #e9ecef;">
                <p style="font-size: 12px; color: #999999; margin: 0;">
                    {{company}} • {{address}}<br>
                    <a href="{{unsubscribe_url}}" style="color: #999999;">Unsubscribe</a>
                </p>
            </td>
        </tr>
    </table>
</body>
</html>'''
            },
            
            'cold_outreach': {
                'subject': '{{personalization}}',
                'preview_text': 'Quick question about {{prospect_company}}',
                'html': '''
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Cold Outreach</title></head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8f9fa;">
    <table role="presentation" style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <tr>
            <td style="padding: 40px;">
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Hi {{first_name}},
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    I noticed {{personalization}} — that's impressive work.
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    I help companies like {{prospect_company}} {{value_proposition}}.
                    We recently helped {{reference_company}} achieve {{result}}.
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Would you be open to a quick 15-minute chat this week?
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Best,<br>
                    <strong>{{sender_name}}</strong><br>
                    <span style="color: #666666;">{{sender_title}} at {{sender_company}}</span>
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px 40px; text-align: center; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                <p style="font-size: 12px; color: #999999; margin: 0;">
                    {{company}} • <a href="{{unsubscribe_url}}" style="color: #999999;">Unsubscribe</a>
                </p>
            </td>
        </tr>
    </table>
</body>
</html>'''
            },
            
            'follow_up': {
                'subject': 'Following up: {{topic}}',
                'preview_text': 'Quick follow-up on our previous conversation',
                'html': '''
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Follow-up</title></head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8f9fa;">
    <table role="presentation" style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <tr>
            <td style="padding: 40px;">
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Hi {{first_name}},
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    I wanted to follow up on our conversation about 
                    <strong>{{topic}}</strong>.
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    {{follow_up_message}}
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Would {{time_proposal}} work for a quick call? I'm also happy to 
                    send over some additional materials in the meantime.
                </p>
                <p style="font-size: 16px; color: #333333; line-height: 1.6;">
                    Looking forward to hearing from you.<br>
                    <strong>{{sender_name}}</strong>
                </p>
            </td>
        </tr>
    </table>
</body>
</html>'''
            },
            
            'newsletter': {
                'subject': '{{issue_number}}: {{headline}}',
                'preview_text': '{{preview_text}}',
                'html': '''
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Newsletter</title></head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8f9fa;">
    <table role="presentation" style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
        <!-- Header -->
        <tr>
            <td style="padding: 30px 40px; text-align: center; background-color: {{primary_color}};">
                <h1 style="color: #ffffff; margin: 0; font-size: 22px;">{{company}} Newsletter</h1>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0; font-size: 14px;">{{issue_date}}</p>
            </td>
        </tr>
        
        <!-- Main Article -->
        <tr>
            <td style="padding: 40px;">
                <h2 style="color: #333333; font-size: 20px; margin: 0 0 15px;">{{headline}}</h2>
                <p style="color: #666666; font-size: 15px; line-height: 1.7;">{{lead_paragraph}}</p>
                <p style="color: #333333; font-size: 15px; line-height: 1.7;">{{article_content}}</p>
                {% if article_cta %}
                <table style="width: 100%; text-align: center; margin: 20px 0;">
                    <tr>
                        <td>
                            <a href="{{article_cta_url}}" 
                               style="background-color: {{primary_color}}; color: #ffffff; 
                                      padding: 12px 28px; text-decoration: none; 
                                      border-radius: 6px; font-weight: 600; 
                                      display: inline-block;">
                                {{article_cta}}
                            </a>
                        </td>
                    </tr>
                </table>
                {% endif %}
            </td>
        </tr>
        
        <!-- Sidebar Items -->
        <tr>
            <td style="padding: 0 40px 30px;">
                <h3 style="color: #333333; font-size: 16px; margin: 0 0 15px; padding-bottom: 10px; border-bottom: 2px solid {{primary_color}};">
                    More This Week
                </h3>
                {% for item in items %}
                <table style="width: 100%; margin-bottom: 15px; padding: 15px; background-color: #f8f9fa; border-radius: 6px;">
                    <tr>
                        <td style="width: 60px; vertical-align: top;">
                            <span style="display: block; width: 40px; height: 40px; background-color: {{primary_color}}; color: #ffffff; 
                                         border-radius: 50%; text-align: center; line-height: 40px; font-weight: bold;">
                                {{loop.index}}
                            </span>
                        </td>
                        <td style="vertical-align: middle;">
                            <a href="{{item.url}}" style="color: #333333; text-decoration: none; font-weight: 600;">
                                {{item.title}}
                            </a>
                            <p style="color: #666666; font-size: 13px; margin: 3px 0 0;">{{item.summary}}</p>
                        </td>
                    </tr>
                </table>
                {% endfor %}
            </td>
        </tr>
        
        <!-- Footer -->
        <tr>
            <td style="padding: 20px 40px; text-align: center; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                <p style="font-size: 12px; color: #999999; margin: 0;">
                    {{company}} • {{address}}<br>
                    <a href="{{unsubscribe_url}}" style="color: #999999;">Unsubscribe</a> | 
                    <a href="{{preferences_url}}" style="color: #999999;">Update Preferences</a>
                </p>
            </td>
        </tr>
    </table>
</body>
</html>'''
            }
        }
    
    def render(self, template_name, context):
        """Render an email template with given context"""
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Render subject
        subject_template = Template(template['subject'])
        subject = subject_template.render(context)
        
        # Render HTML
        html_template = Template(template['html'])
        html = html_template.render(context)
        
        return {
            'subject': subject,
            'html': html,
            'preview_text': template.get('preview_text', ''),
            'plain_text': self._extract_text(html)
        }
    
    def _extract_text(self, html):
        """Extract plain text from HTML for email clients that don't support HTML"""
        import re
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def generate_cold_email(self, prospect_name, prospect_company, sender_name, 
                           sender_company, personalization, value_prop, reference, 
                           result, time_proposal='next Tuesday or Wednesday'):
        """Generate a personalized cold outreach email"""
        return self.render('cold_outreach', {
            'first_name': prospect_name.split()[0] if prospect_name else 'there',
            'prospect_company': prospect_company,
            'sender_name': sender_name,
            'sender_title': 'Founder/CEO',
            'sender_company': sender_company,
            'personalization': personalization,
            'value_proposition': value_prop,
            'reference_company': reference.get('company', 'a similar company'),
            'result': reference.get('result', 'significant results'),
            'time_proposal': time_proposal,
            'company': sender_company,
            'unsubscribe_url': '#'
        })
    
    def generate_follow_up(self, first_name, topic, follow_up_message, 
                          sender_name, time_proposal='next Tuesday or Wednesday'):
        """Generate a follow-up email"""
        return self.render('follow_up', {
            'first_name': first_name,
            'topic': topic,
            'follow_up_message': follow_up_message,
            'sender_name': sender_name,
            'time_proposal': time_proposal
        })
    
    def generate_welcome_email(self, first_name, company, primary_color='#2563eb',
                               get_started_url='#', help_url='#', unsubscribe_url='#'):
        """Generate a welcome email"""
        return self.render('welcome', {
            'first_name': first_name,
            'company': company,
            'primary_color': primary_color,
            'get_started_url': get_started_url,
            'help_url': help_url,
            'unsubscribe_url': unsubscribe_url,
            'address': '123 Business St, City, State 12345'
        })
    
    def generate_newsletter(self, company, issue_number, issue_date, headline, 
                           lead_paragraph, article_content, article_cta, 
                           article_cta_url, items, primary_color='#2563eb',
                           unsubscribe_url='#', preferences_url='#'):
        """Generate a newsletter email"""
        return self.render('newsletter', {
            'company': company,
            'issue_number': issue_number,
            'issue_date': issue_date,
            'headline': headline,
            'lead_paragraph': lead_paragraph,
            'article_content': article_content,
            'article_cta': article_cta,
            'article_cta_url': article_cta_url,
            'items': items,
            'primary_color': primary_color,
            'unsubscribe_url': unsubscribe_url,
            'preferences_url': preferences_url,
            'address': '123 Business St, City, State 12345'
        })
```

## Common Workflows

### Workflow: Cold Outreach Sequence
1. Research prospect (company, recent news, pain points)
2. Write personalized opening referencing prospect context
3. State clear value proposition
4. Include social proof (reference company + result)
5. Soft CTA (meeting request)
6. Follow up 3-5 days later
7. Second follow-up 5-7 days after first

### Workflow: Welcome Series
1. Immediate welcome email (account setup)
2. Day 2: Feature highlight #1
3. Day 5: Feature highlight #2
4. Day 7: Customer success story
5. Day 14: Check-in/feedback request

### Workflow: Newsletter Production
1. Collect content from team/sources
2. Write headline and lead paragraph
3. Format 3-5 items with summaries
4. Add CTA for main article
5. Design and send

## Best Practices
- **Subject lines**: Keep under 50 characters, personalize when possible
- **Preheader**: Complement subject line, create curiosity
- **CTA**: Single clear action, contrasting color
- **Mobile**: Test on mobile, keep width to 600px
- **Accessibility**: Alt text for images, proper contrast
- **Unsubscribe**: Make it easy, comply with regulations

## Integration with Other Skills
- `docx` — create email templates as Word documents
- `pdf` — export templates as PDF for reference
- `email-templates` — for email campaign design
- `meeting-notes` — extract action items for follow-up emails
- `calendar-automation` — schedule email sends
