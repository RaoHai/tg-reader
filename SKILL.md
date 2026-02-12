---
name: tg-reader
description: Read Telegram messages using Telethon (user API). Use when needing to read group/channel messages including bot messages, list chats and their IDs, or login to Telegram. Triggers include "读取TG消息", "拉群消息", "看看群里说了什么", "列出TG对话", "登录Telegram".
---

# TG Reader

用 Telethon 以用户身份读取 Telegram 消息，可以看到所有消息包括 bot 消息。

## 配置

配置文件：`config.json`

```json
{
  "api_id": "你的api_id",
  "api_hash": "你的api_hash", 
  "session_name": "tg_session",
  "phone": "+86手机号",
  "password": "两步验证密码(可选)",
  "chat_id": -1001234567890
}
```

获取 api_id/api_hash：https://my.telegram.org

## 使用

### 首次登录

```bash
# 1. 发送验证码
python3 scripts/login.py

# 2. 输入验证码（如有两步验证，加密码参数）
python3 scripts/login_step2.py <验证码> [密码]
```

### 读取消息

```bash
# 读取消息（需先在 config.json 设置 chat_id）
python3 scripts/reader.py --limit 100
```

### 列出对话

```bash
# 查看所有对话及 ID
python3 scripts/list_chats.py
```

## 依赖

```bash
pip install telethon
```
