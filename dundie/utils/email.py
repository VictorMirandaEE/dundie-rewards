"""Email module for dundie."""

import re
import smtplib
from email.mime.text import MIMEText

from pydantic import EmailStr

from dundie.settings import (
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_TIMEOUT,
    SMTP_USERNAME,
)
from dundie.utils.log import get_logger

regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"  # noqa E501


def check_valid_email(address: str) -> bool:
    """Check if email is valid.

    Args:
        address (str): Email address.

    Returns:
        bool: True if email is valid, False otherwise.
    """
    return bool(re.fullmatch(regex, address))


def send_email(
    sender: str, recipient: EmailStr | list[EmailStr], subject: str, body: str
) -> None:
    """
    Send an email using the specified parameters.

    Args:
        sender (str): The email address of the sender.
        recipient (EmailStr | list[EmailStr]): A single recipient email address
          or a list of recipient email addresses.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Raises:
        Exception: If there is an error sending the email, it logs the error
          message.
    """
    log = get_logger()

    log.debug(
        "Sending email from '%s' to '%s' with subject '%s' and body '%s'",
        sender,
        recipient,
        subject,
        body,
    )

    if not isinstance(recipient, list):
        recipient = [recipient]
    try:
        with smtplib.SMTP(
            host=SMTP_HOST,
            port=SMTP_PORT,
            timeout=SMTP_TIMEOUT,
        ) as server:
            message = MIMEText(body)
            message["From"] = sender
            message["To"] = (",").join(recipient)
            message["Subject"] = subject
            server.user = SMTP_USERNAME
            server.password = SMTP_PASSWORD
            server.auth_plain()
            server.sendmail(sender, recipient, message.as_string())
    except Exception as error_msg:
        log.error("Error sending email to %s: %s", recipient, error_msg)
