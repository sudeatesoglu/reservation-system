import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings
from app.schemas import NotificationEvent, EmailMessage
from app.templates import template_renderer

settings = get_settings()


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    async def send_email(message: EmailMessage) -> bool:
        """Send an email"""
        if not settings.EMAIL_ENABLED:
            print(f"Email disabled. Would send to: {message.to_email}")
            print(f"Subject: {message.subject}")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = message.subject
            msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg["To"] = message.to_email
            
            # Add text and HTML parts
            text_part = MIMEText(message.body_text, "plain")
            html_part = MIMEText(message.body_html, "html")
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True
            )
            print(f"Email sent to: {message.to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


class NotificationService:
    """Service for processing notifications"""
    
    @staticmethod
    async def process_notification(event: NotificationEvent) -> bool:
        """Process a notification event"""
        print(f"Processing notification: {event.event_type} for user {event.username}")
        
        # Build context for template
        context = {
            "username": event.username,
            "resource_name": event.resource_name,
            "date": event.date,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "reservation_id": event.reservation_id
        }
        
        # Add additional data if present
        if event.additional_data:
            context.update(event.additional_data)
        
        # Render email content
        subject, html_body, text_body = template_renderer.render(
            event.event_type, context
        )
        
        # If we have an email, send it
        if event.email:
            email_message = EmailMessage(
                to_email=event.email,
                subject=subject,
                body_html=html_body,
                body_text=text_body
            )
            return await EmailService.send_email(email_message)
        else:
            # Log the notification (email not available)
            print(f"No email for user {event.username}, notification logged only")
            print(f"  Event: {event.event_type}")
            print(f"  Resource: {event.resource_name}")
            print(f"  Date: {event.date} {event.start_time}-{event.end_time}")
            return True
