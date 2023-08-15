from typing import List, Literal, Optional

from pydantic import Field, AnyUrl, EmailStr, BaseModel, AnyHttpUrl


class AnySmtpUrl(AnyUrl):
    allowed_schemes = {"smtp", "smtps"}

    __slots__ = ()


class MailPushAccount(BaseModel):
    name: str = Field(alias="name")
    """
    Account name
    """
    type: Literal["mail"] = Field(alias="type")
    """
    Account type
    """
    url: AnySmtpUrl = Field(alias="url")
    """
    Account URL

    SMTP server URL, e.g. smtp://smtp.gmail.com:465
    """
    username: str = Field(alias="username")
    """
    Account username

    SMTP username (Mail address)
    """
    password: Optional[str] = Field(alias="password")
    """
    Account password

    SMTP password
    """
    targets: List[EmailStr] = Field(alias="targets", default_factory=list)
    """
    Push targets

    Target mail address list
    """


class FeishuPushAccount(BaseModel):
    name: str = Field(alias="name")
    """
    Account name
    """
    type: Literal["feishu"] = Field(alias="type")
    """
    Account type
    """
    url: AnyHttpUrl = Field(alias="url")
    """
    Account URL

    Feishu Webhook URL, e.g. https://open.feishu.cn/open-apis/bot/v2/hook/xxx
    """
    password: Optional[str] = Field(alias="password")
    """
    Account password

    Optional, Feishu Webhook Secret
    """
