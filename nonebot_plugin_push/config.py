from typing import List, Union

from pydantic import Extra, Field, BaseModel

from .model import MailPushAccount, FeishuPushAccount


class Config(BaseModel, extra=Extra.ignore):
    push_accounts: List[Union[MailPushAccount, FeishuPushAccount]] = Field(
        alias="push_accounts", default_factory=list
    )
