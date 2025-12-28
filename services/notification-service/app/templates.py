from jinja2 import Environment, BaseLoader

# Email templates
TEMPLATES = {
    "reservation_created": {
        "subject": "Reservation Confirmed - {resource_name}",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .details { background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Reservation Confirmed</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{{ username }}</strong>,</p>
            <p>Your reservation has been successfully confirmed!</p>
            
            <div class="details">
                <h3>Reservation Details</h3>
                <p><strong>Resource:</strong> {{ resource_name }}</p>
                <p><strong>Date:</strong> {{ date }}</p>
                <p><strong>Time:</strong> {{ start_time }} - {{ end_time }}</p>
                <p><strong>Reservation ID:</strong> {{ reservation_id }}</p>
            </div>
            
            <p>Please arrive on time. If you need to cancel, please do so at least 1 hour before your reservation.</p>
        </div>
        <div class="footer">
            <p>This is an automated message from the Reservation System.</p>
        </div>
    </div>
</body>
</html>
        """,
        "text": """
Reservation Confirmed!

Hello {{ username }},

Your reservation has been successfully confirmed!

Reservation Details:
- Resource: {{ resource_name }}
- Date: {{ date }}
- Time: {{ start_time }} - {{ end_time }}
- Reservation ID: {{ reservation_id }}

Please arrive on time. If you need to cancel, please do so at least 1 hour before your reservation.

---
This is an automated message from the Reservation System.
        """
    },
    
    "reservation_cancelled": {
        "subject": "Reservation Cancelled - {resource_name}",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #f44336; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .details { background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Reservation Cancelled</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{{ username }}</strong>,</p>
            <p>Your reservation has been cancelled.</p>
            
            <div class="details">
                <h3>Cancelled Reservation Details</h3>
                <p><strong>Resource:</strong> {{ resource_name }}</p>
                <p><strong>Date:</strong> {{ date }}</p>
                <p><strong>Time:</strong> {{ start_time }} - {{ end_time }}</p>
                <p><strong>Reservation ID:</strong> {{ reservation_id }}</p>
                {% if reason %}
                <p><strong>Reason:</strong> {{ reason }}</p>
                {% endif %}
            </div>
            
            <p>If you didn't request this cancellation, please contact support.</p>
        </div>
        <div class="footer">
            <p>This is an automated message from the Reservation System.</p>
        </div>
    </div>
</body>
</html>
        """,
        "text": """
Reservation Cancelled

Hello {{ username }},

Your reservation has been cancelled.

Cancelled Reservation Details:
- Resource: {{ resource_name }}
- Date: {{ date }}
- Time: {{ start_time }} - {{ end_time }}
- Reservation ID: {{ reservation_id }}
{% if reason %}- Reason: {{ reason }}{% endif %}

If you didn't request this cancellation, please contact support.

---
This is an automated message from the Reservation System.
        """
    },
    
    "reservation_reminder": {
        "subject": "Reminder: Upcoming Reservation - {resource_name}",
        "html": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #2196F3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .details { background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⏰ Reservation Reminder</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{{ username }}</strong>,</p>
            <p>This is a reminder about your upcoming reservation.</p>
            
            <div class="details">
                <h3>Reservation Details</h3>
                <p><strong>Resource:</strong> {{ resource_name }}</p>
                <p><strong>Date:</strong> {{ date }}</p>
                <p><strong>Time:</strong> {{ start_time }} - {{ end_time }}</p>
            </div>
            
            <p>Please arrive on time!</p>
        </div>
        <div class="footer">
            <p>This is an automated message from the Reservation System.</p>
        </div>
    </div>
</body>
</html>
        """,
        "text": """
Reservation Reminder

Hello {{ username }},

This is a reminder about your upcoming reservation.

Reservation Details:
- Resource: {{ resource_name }}
- Date: {{ date }}
- Time: {{ start_time }} - {{ end_time }}

Please arrive on time!

---
This is an automated message from the Reservation System.
        """
    }
}


class TemplateRenderer:
    """Render email templates"""
    
    def __init__(self):
        self.env = Environment(loader=BaseLoader())
    
    def render(self, event_type: str, context: dict) -> tuple:
        """Render template for event type"""
        if event_type not in TEMPLATES:
            event_type = "reservation_created"  # fallback
        
        template = TEMPLATES[event_type]
        
        # Render subject
        subject = template["subject"].format(**context)
        
        # Render HTML body
        html_template = self.env.from_string(template["html"])
        html_body = html_template.render(**context)
        
        # Render text body
        text_template = self.env.from_string(template["text"])
        text_body = text_template.render(**context)
        
        return subject, html_body, text_body


template_renderer = TemplateRenderer()
