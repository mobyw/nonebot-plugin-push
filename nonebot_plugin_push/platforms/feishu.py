import hmac
import time
import base64
import hashlib
from typing import List, Union, Optional

from nonebot import logger
from pydantic import BaseModel
from nonebot.drivers import Driver, Request, ForwardDriver

from .. import status
from .base import BasePush
from ..config import FeishuPushAccount
from ..message import Message, MessageSegment


class Content(BaseModel):
    tag: str
    content: str


class TextContent(Content):
    tag: str = "plain_text"
    content: str


class MarkdownContent(Content):
    tag: str = "lark_md"
    content: str


class Header(BaseModel):
    title: TextContent


class Element(BaseModel):
    tag: str = "div"
    text: Content


class Card(BaseModel):
    header: Header
    elements: List[Element]


class FeishuMessage(BaseModel):
    msg_type: str = "interactive"
    card: Card
    timestamp: Optional[str] = None
    sign: Optional[str] = None


class FeishuPush(BasePush):
    """
    Feishu Webhook Push
    """

    def __init__(self, config: FeishuPushAccount, driver: Driver):
        if not isinstance(driver, ForwardDriver):
            raise RuntimeError(
                f"Current driver {driver} does not support "
                "forward connections! FeishuPush need a ForwardDriver to work."
            )
        super().__init__(config.name, config.type)
        self.driver = driver
        self.url = config.url
        self.password = config.password

    async def send(
        self, message: Union[str, Message, MessageSegment], title: str = "NoneBot Push"
    ) -> int:
        full_message = Message()
        full_message += message
        contents: List[Content] = []
        for seg in full_message:
            if seg.type == "text":
                contents.append(TextContent(content=seg.data["text"]))
            elif seg.type == "markdown":
                contents.append(MarkdownContent(content=seg.data["text"]))
        send_message = FeishuMessage(
            card=Card(
                header=Header(title=TextContent(content=title)),
                elements=[Element(text=content) for content in contents],
            )
        )
        if self.password is not None:
            timestamp = str(int(time.time()))
            send_message.timestamp = timestamp
            send_message.sign = self.generate_sign(timestamp)
        request = Request("POST", self.url, json=send_message.dict())
        response = await self.driver.request(request)
        if response.status_code != 200:
            logger.error(
                f"Push to {self.name} failed with status code "
                + f"{response.status_code}: {response.content}"
            )
            return status.FAILED
        logger.info(f"Push to {self.name} succeeded.")
        return status.SUCCESS

    def generate_sign(self, timestamp: str):
        """
        Generate sign for feishu webhook
        """
        s = f"{timestamp}\n{self.password}"
        c = hmac.new(s.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(c).decode("utf-8")
