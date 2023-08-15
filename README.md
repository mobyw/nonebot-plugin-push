<!-- markdownlint-disable MD033 MD036 MD041-->

<div align="center">

# nonebot-plugin-push

_✨ 消息推送插件 ✨_

</div>

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonebot-plugin-push)
![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-push)
![GitHub](https://img.shields.io/github/license/mobyw/nonebot-plugin-push)

## 简介

本插件提供通过邮件、Feishu Webhook 方式进行消息推送，支持纯文本与 Markdown 格式的内容。

## 安装步骤

### 使用 `nb-cli` 安装（推荐）

```bash
nb plugin install nonebot-plugin-push
```

### 使用 `pip` 安装

```bash
pip install nonebot-plugin-push
```

需要在 bot 根目录 `pyproject.toml` 文件中 [tool.nonebot] 部分添加：

```python
plugins = ["nonebot_plugin_push"]
```

## 配置

### 账号配置

当前支持通过邮件和 Feishu Webhook 进行推送，配置示例如下：

```dotenv
PUSH_ACCOUNTS='
[
  {
    "name": "push1",
    "type": "mail",
    "url": "smtp://smtp.example.com:465",
    "username": "name@example.com",
    "password": "password",
    "targets": [ "to@example.com" ]
  },
  {
    "name": "push2",
    "type": "feishu",
    "url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx",
    "password": "password"
  }
]
'
```

如需按名称获取推送账号，请保证 `name` 字段唯一，下表为单个账号配置中各字段的说明：

|            | Mail                  | Feishu Webhook     |
| ---------- | --------------------- | ------------------ |
| `name`     | 推送名称              | 推送名称           |
| `type`     | 固定为 "mail"         | 固定为 "feishu"    |
| `url`      | SMTP 连接主机与端口号 | webhook url        |
| `username` | 账号名（邮箱账号）    | -                  |
| `password` | SMTP 连接密钥         | 签名校验密钥，可选 |
| `targets`  | 推送邮箱列表          | -                  |

### Driver

若使用 Feishu Webhook，需要参考 [driver](https://nonebot.dev/docs/appendices/config#driver) 配置项，添加 `ForwardDriver` 支持。

## 跨插件使用

导入方式：

```python
from nonebot import require
require("nonebot_plugin_push")
```

使用方式：

```python
from nonebot_plugin_push import MessageSegment, get_push, get_push_list

message = MessageSegment.markdown('**Markdown**<font color="red">文本</font>') + '普通文本'
push = get_push()
if push is not None:
    await push.send(message, "推送消息标题（可选）")
```

获取特定的推送账号：

```python
from nonebot_plugin_push import get_push, get_push_list

# 获取第一个推送账号
push = get_push()
# 获取一个指定名称的推送账号
push = get_push(name="push1")
# 获取一个指定类型的推送账号
push = get_push(type="mail")
# 获取指定类型的推送账号列表
push = get_push_list(type="feishu")
```

## 其他说明

Feishu Webhook 仅支持部分 Markdown 语法，具体请查阅 [Markdown 模块](https://open.feishu.cn/document/common-capabilities/message-card/message-cards-content/using-markdown-tags#abc9b025) 文档。
