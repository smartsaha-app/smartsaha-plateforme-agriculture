import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

class ResendEmailBackend(BaseEmailBackend):
    """
    Un backend d'email Django personnalisé pour Resend.
    """
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, 'RESEND_API_KEY', None)
        if self.api_key:
            resend.api_key = self.api_key

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        if not self.api_key:
            logger.error("RESEND_API_KEY n'est pas configuré.")
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY est manquant dans les réglages.")
            return 0

        sent_count = 0
        for message in email_messages:
            if self._send(message):
                sent_count += 1
        return sent_count

    def _send(self, message: EmailMessage):
        try:
            params = {
                "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
                "to": message.to,
                "subject": message.subject,
                "text": message.body,
            }

            # Gérer le HTML si présent
            if hasattr(message, 'alternatives') and message.alternatives:
                for content, mimetype in message.alternatives:
                    if mimetype == 'text/html':
                        params["html"] = content
                        break
            elif message.content_subtype == 'html':
                params["html"] = message.body

            # Gérer les pièces jointes
            if message.attachments:
                attachments = []
                for attachment in message.attachments:
                    # attachment can be (filename, content, mimetype)
                    filename, content, mimetype = attachment
                    attachments.append({
                        "filename": filename,
                        "content": content if isinstance(content, str) else content.decode('latin-1'),
                    })
                params["attachments"] = attachments

            resend.Emails.send(params)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi via Resend : {str(e)}")
            if not self.fail_silently:
                raise
            return False
