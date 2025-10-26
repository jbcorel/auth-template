import structlog
from fastapi import UploadFile
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import SecretStr, ValidationError


logger = structlog.get_logger()


class Mailer:
    def __init__(self, host: str, port: int, username: str, password: SecretStr, from_email: str, *, starttls: bool):
        self._mailer = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=username,
                MAIL_PASSWORD=password,
                MAIL_PORT=port,
                MAIL_SERVER=host,
                MAIL_STARTTLS=starttls,
                MAIL_SSL_TLS=False,
                MAIL_FROM=from_email,
            )
        )

    async def send_mail(
        self,
        subject: str,
        body: str,
        recipients: list[str],
        attachments: list[UploadFile] | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
    ):
        if attachments is None:
            attachments = []
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []

        try:
            msg = MessageSchema(
                recipients=recipients,
                attachments=attachments,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                subtype=MessageType.html,
            )
        except ValidationError as e:
            logger.exception(
                "Can't create mail message",
                extra={
                    "recipients": recipients,
                    "attachments": attachments,
                    "subject": subject,
                    "body": body,
                    "cc": cc,
                    "bcc": bcc,
                    "subtype": MessageType.html,
                },
            )
        else:
            await self._mailer.send_message(message=msg)
