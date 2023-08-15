import html
from typing import Union
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import markdown
import aiosmtplib
from nonebot import logger
from nonebot.drivers import Driver

from .. import status
from .base import BasePush
from ..config import MailPushAccount
from ..message import Message, MessageSegment


class MailPush(BasePush):
    """
    Mail SMTP Push
    """

    def __init__(self, config: MailPushAccount, driver: Driver):
        super().__init__(config.name, config.type)
        self.driver = driver
        self.url = config.url
        self.username = config.username
        self.password = config.password
        self.targets = config.targets

    async def send(
        self, message: Union[str, Message, MessageSegment], title: str = "NoneBot Push"
    ) -> int:
        full_message = Message()
        full_message += message
        send_message = MIMEMultipart("alternative")
        send_message["From"] = self.username
        send_message["Subject"] = title
        for seg in full_message:
            if seg.type == "text":
                send_message.attach(
                    MIMEText(html.escape(seg.data["text"]), "html", "utf-8")
                )
            elif seg.type == "markdown":
                send_message.attach(
                    MIMEText(markdown.markdown(seg.data["text"]), "html", "utf-8")
                )
        failed_num = 0
        for target in self.targets:
            send_message["To"] = target
            try:
                await aiosmtplib.send(
                    message=send_message,
                    hostname=self.url.host,
                    port=int(self.url.port or "465"),
                    username=self.username,
                    password=self.password,
                    use_tls=False if self.url.port == "25" else True,
                )
            except Exception as e:
                failed_num += 1
                logger.error(
                    f"Push to {self.name} failed with exception "
                    + f"{type(e).__name__}: {e}"
                )
                continue
        if failed_num == len(self.targets):
            return status.FAILED
        if failed_num > 0:
            return status.PARTIAL
        logger.info(f"Push to {self.name} succeeded.")
        return status.SUCCESS
