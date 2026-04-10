# Email Setup

The Resume Generator sends resumes via [Resend](https://resend.com/), a developer-friendly email API. Email sending is implemented in `portfolio/email.py`.

---

## Resend Configuration

### 1. Create a Resend Account

1. Sign up at [resend.com](https://resend.com/).
2. Verify your sending domain (or use Resend's sandbox for testing).
3. Generate an API key from the Resend dashboard.

### 2. Set Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `RESEND_API_KEY` | `re_xxxxxxxxxxxxxxxxx` | Your Resend API key |
| `FROM_EMAIL` | `resumes@yourdomain.com` | Must be an address on a verified domain in Resend |

**Local development:**
```bash
export RESEND_API_KEY="re_your_api_key_here"
export FROM_EMAIL="resumes@yourdomain.com"
```

**Railway:**
Set both variables in the Railway dashboard under your web service's **Variables** tab.

### 3. Verify Your Domain

In the Resend dashboard:
1. Go to **Domains**.
2. Add your sending domain.
3. Add the DNS records Resend provides (SPF, DKIM, DMARC).
4. Wait for verification (usually minutes, sometimes hours).

Until your domain is verified, Resend only allows sending to the account owner's email address.

---

## Email Templates

Email templates are stored as `EmailTemplate` models in the database, managed through the Django admin.

### Template Fields

| Field | Description |
|-------|-------------|
| `name` | Human-readable name (e.g., "Standard Introduction") |
| `slug` | URL-safe identifier (e.g., `standard-introduction`) |
| `subject_template` | Subject line with placeholder variables |
| `body_template` | Email body with placeholder variables |
| `is_default` | Whether this is the default template. Only one template should have this checked. |

### Creating a Template

1. Navigate to **Portfolio > Email Templates** in the admin.
2. Click **Add Email Template**.
3. Fill in the name, slug, subject, and body.
4. Use placeholder variables (see below) for dynamic content.
5. Check **Is default** if this should be the default template.
6. Click **Save**.

---

## Placeholder Variables

Templates support placeholder variables that are replaced with actual values at send time. Use Python string formatting syntax: `{variable_name}`.

### Available Placeholders

| Placeholder | Source | Example Value |
|-------------|--------|---------------|
| `{recipient_name}` | Recipient.name | "Jane Smith" |
| `{recipient_company}` | Recipient.company | "Acme Corporation" |
| `{recipient_role}` | Recipient.role | "Senior Recruiter" |
| `{recipient_job_title}` | Recipient.job_title | "Lead Data Scientist" |
| `{sender_name}` | PersonalInfo.name | "Dheeraj Chand" |
| `{sender_title}` | PersonalInfo.title | "Data Scientist & GIS Specialist" |
| `{sender_email}` | PersonalInfo.email | "dheeraj@example.com" |
| `{sender_phone}` | PersonalInfo.phone | "(555) 123-4567" |
| `{sender_website}` | PersonalInfo.website | "https://example.com" |
| `{archetype_name}` | ResumeArchetype.name | "Data Science" |
| `{instance_name}` | ResumeInstance.name | "Acme Corp Data Science Role" |

### Example Template

**Subject:**
```
{sender_name} — Resume for {recipient_job_title} at {recipient_company}
```

**Body:**
```
Dear {recipient_name},

I am writing to express my interest in the {recipient_job_title} position at {recipient_company}. Please find my resume attached.

As a {sender_title}, I bring experience that aligns well with the requirements of this role. I would welcome the opportunity to discuss how my background can contribute to your team.

Thank you for your consideration.

Best regards,
{sender_name}
{sender_email}
{sender_phone}
{sender_website}
```

### Subject Override

If a ResumeInstance has a `subject_override` set, it replaces the template's subject line entirely. The override also supports the same placeholder variables.

---

## The Sending Flow

When you trigger the **Send Resume** admin action, here is exactly what happens:

### Step-by-Step

1. **Validation**
   - Checks that the selected ResumeInstance(s) have recipients with email addresses.
   - Checks that `RESEND_API_KEY` and `FROM_EMAIL` are configured.
   - Checks that at least one EmailTemplate exists.

2. **Resume Generation**
   - Calls `build_resume_data_from_db()` with the instance's archetype slug.
   - Applies `summary_override` from the instance if present.
   - Generates a PDF via `ResumeGenerator`.

3. **Template Rendering**
   - Selects the EmailTemplate:
     - Uses the default template (`is_default = True`).
   - Applies `subject_override` from the instance if present.
   - Renders the subject and body by replacing placeholder variables with actual values.

4. **Email Sending**
   - Calls the Resend API with:
     - `from`: `FROM_EMAIL` environment variable.
     - `to`: Recipient's email address.
     - `subject`: Rendered subject line.
     - `html` or `text`: Rendered body.
     - `attachments`: The generated PDF file.

5. **Logging**
   - Creates a `GenerationRecord` with:
     - `instance`: The ResumeInstance.
     - `archetype_slug`: The archetype used.
     - `format_type`: `pdf`.
     - `output_type`: `email`.
     - `was_emailed`: `True`.
     - `generated_at`: Current timestamp.

6. **Follow-up Tracking**
   - Sets `follow_up_date` on the instance (typically 5-7 days from now).
   - Updates `follow_up_status` to indicate a resume has been sent.

### Sequence Diagram (Text)

```
Admin                     email.py               Resend API          Database
  │                          │                       │                  │
  │── Send Resume action ──>│                       │                  │
  │                          │── build_resume_data ──────────────────>│
  │                          │<── data dict ─────────────────────────│
  │                          │── ResumeGenerator ──>│                  │
  │                          │<── PDF bytes ────────│                  │
  │                          │── render template ───────────────────>│
  │                          │<── subject + body ───────────────────│
  │                          │── send email ────────>│                  │
  │                          │<── success ──────────│                  │
  │                          │── create GenerationRecord ──────────>│
  │                          │── update follow_up ─────────────────>│
  │<── success message ─────│                       │                  │
```

---

## Testing Email Locally

### Option 1: Resend Sandbox

Use Resend's sandbox mode — you can only send to the account owner's email, but it works without domain verification.

### Option 2: Console Backend

For development without sending real emails, you can temporarily configure Django's console email backend. However, note that the Resend integration bypasses Django's email system, so this only works if you modify `email.py` to use Django's `send_mail()` instead.

### Option 3: Send to Yourself

1. Create a Recipient with your own email address.
2. Create a ResumeInstance pointing to that recipient.
3. Use the Send Resume action.
4. Check your inbox.

---

## Troubleshooting

### "RESEND_API_KEY not configured"
Set the `RESEND_API_KEY` environment variable. In Railway, add it under Variables.

### "FROM_EMAIL not configured"
Set the `FROM_EMAIL` environment variable.

### "Domain not verified"
Your sending domain must be verified in Resend. Check the Resend dashboard for DNS record instructions.

### Email sent but not received
1. Check the Resend dashboard for delivery status.
2. Check the recipient's spam/junk folder.
3. Verify DNS records (SPF, DKIM, DMARC) are correctly configured.

### "No default email template found"
Create an EmailTemplate in the admin with `is_default = True`.
