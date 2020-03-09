import smtplib
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

logger = logging.getLogger(__name__)


def send_mail(subject, sender, receiver, text, html_content):
    server = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    sender = sender if sender else settings.DEFAULT_SENDER_EMAIL

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    html = html_content
    text = text
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    import socket
    socket.setdefaulttimeout(2)

    try:
        s = smtplib.SMTP_SSL(server, port)
        s.login(username, password)
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
    except Exception, error:
        logger.info(error)
        try:
            s = smtplib.SMTP(server, port)
            s.starttls()
            s.login(username, password)
            s.sendmail(sender, receiver, msg.as_string())
            s.quit()
        except Exception, error:
            logger.info(error)
            return False
    return True
