"""
Email sending via Resend API — send resumes to recipients with template support.
Uses onboarding@resend.dev as sender with reply-to pointing to the real email.
"""

import logging
import os

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "onboarding@resend.dev")
REPLY_TO_EMAIL = os.environ.get("REPLY_TO_EMAIL", "dheeraj.chand@gmail.com")


def send_resume_email(instance, resume_buffer, filename, email_template=None):
    """Send a resume to the instance's recipient via Resend API.

    Args:
        instance: ResumeInstance with recipient
        resume_buffer: BytesIO containing the generated resume
        filename: e.g., "dheeraj_chand_data_engineering_brief.pdf"
        email_template: EmailTemplate instance (optional, uses default if None)

    Returns:
        dict with send result or error
    """
    if not RESEND_API_KEY:
        return {"error": "RESEND_API_KEY not configured"}

    if not instance.recipient or not instance.recipient.email:
        return {"error": "Instance has no recipient with email address"}

    import resend
    resend.api_key = RESEND_API_KEY

    # Build template context
    from .models import PersonalInfo
    try:
        info = PersonalInfo.objects.get()
        your_name = info.name
    except PersonalInfo.DoesNotExist:
        your_name = "Resume Generator"

    context = {
        "recipient_name": instance.recipient.name,
        "job_title": instance.recipient.job_title or instance.archetype.name,
        "company": instance.recipient.company,
        "archetype_name": instance.archetype.name,
        "your_name": your_name,
    }

    # Use template or defaults for subject and body
    if email_template:
        subject = email_template.render_subject(**context)
        body = email_template.render_body(**context)
    else:
        from .models import EmailTemplate
        default = EmailTemplate.objects.filter(is_default=True).first()
        if default:
            subject = default.render_subject(**context)
            body = default.render_body(**context)
        else:
            subject = f"{your_name} — {context['job_title']}"
            body = (
                f"Dear {context['recipient_name']},\n\n"
                f"Please find attached my resume for the {context['job_title']} position "
                f"at {context['company']}.\n\n"
                f"Best regards,\n{your_name}"
            )

    # Instance-level subject override takes precedence
    if hasattr(instance, "subject_override") and instance.subject_override:
        subject = instance.subject_override

    # Add reply-to disclaimer if sending from a different address
    if FROM_EMAIL != REPLY_TO_EMAIL:
        body += (
            f"\n\n---\n"
            f"Note: This email was sent from an automated system. "
            f"Please reply directly to {REPLY_TO_EMAIL}"
        )

    # Read buffer content
    resume_buffer.seek(0)
    file_content = resume_buffer.read()

    # Determine content type from filename
    ext = filename.rsplit(".", 1)[-1].lower()
    content_types = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "rtf": "application/rtf",
        "md": "text/markdown",
    }

    try:
        import base64
        result = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [instance.recipient.email],
            "reply_to": REPLY_TO_EMAIL,
            "subject": subject,
            "text": body,
            "attachments": [
                {
                    "filename": filename,
                    "content": base64.b64encode(file_content).decode("utf-8"),
                    "content_type": content_types.get(ext, "application/octet-stream"),
                }
            ],
        })
        logger.info(f"Email sent to {instance.recipient.email}: {result}")
        return {"success": True, "id": result.get("id", "")}
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        return {"error": str(e)}
