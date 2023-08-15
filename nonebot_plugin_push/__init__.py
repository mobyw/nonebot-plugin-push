from typing import List, Union, Literal, Optional

from nonebot import get_driver
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from .config import Config
from .platforms import MailPush, FeishuPush
from .model import MailPushAccount, FeishuPushAccount

__plugin_meta__ = PluginMetadata(
    name="消息推送插件",
    description="通过邮件、Feishu Webhook 等方式推送消息",
    usage="请参考插件文档",
    type="library",
    homepage="https://github.com/mobyw/nonebot-plugin-push",
    config=Config,
    supported_adapters=None,
)

driver = get_driver()
plugin_config = Config(**driver.config.dict())


def get_push_by_account(account: Union[FeishuPushAccount, MailPushAccount]):
    if isinstance(account, FeishuPushAccount):
        return FeishuPush(account, driver)
    if isinstance(account, MailPushAccount):
        return MailPush(account, driver)


def get_push(
    name: Optional[str] = None, type: Optional[Literal["mail", "feishu"]] = None
) -> Union[FeishuPush, MailPush, None]:
    if not plugin_config.push_accounts:
        logger.warning("No push account found")
        return None
    if name:
        for account in plugin_config.push_accounts:
            if account.name == name:
                return get_push_by_account(account)
        return None
    if type:
        for account in plugin_config.push_accounts:
            if account.type == type:
                return get_push_by_account(account)
        return None
    return get_push_by_account(plugin_config.push_accounts[0])


def get_push_list(
    type: Optional[Literal["mail", "feishu"]] = None
) -> List[Union[FeishuPush, MailPush]]:
    push_list: List[Union[FeishuPush, MailPush]] = []
    if type:
        for account in plugin_config.push_accounts:
            if account.type == type:
                push = get_push_by_account(account)
                push_list.append(push) if push else None
        return push_list
    for account in plugin_config.push_accounts:
        push = get_push_by_account(account)
        push_list.append(push) if push else None
    return push_list


from .message import Message as Message
from .message import MessageSegment as MessageSegment
