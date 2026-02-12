#!/usr/bin/env python3
"""
Telethon 登录脚本 - 步骤1：发送验证码
"""

import asyncio
import json
import os
from pathlib import Path
from telethon import TelegramClient

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
SESSION_DIR = SKILL_DIR / "sessions"


def load_config():
    if not CONFIG_FILE.exists():
        print(f"错误：配置文件不存在 {CONFIG_FILE}")
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)


async def send_code():
    config = load_config()
    if not config:
        return

    api_id = int(config["api_id"])
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "tg_session")
    phone = config.get("phone") or os.getenv("TG_PHONE")

    if not phone:
        print("错误：需要在 config.json 中设置 phone 或设置环境变量 TG_PHONE")
        return

    SESSION_DIR.mkdir(exist_ok=True)
    session_path = SESSION_DIR / session_name

    client = TelegramClient(str(session_path), api_id, api_hash)
    await client.connect()

    if await client.is_user_authorized():
        print("已经登录过了")
        me = await client.get_me()
        print(f"当前账号: {me.first_name} (@{me.username})")
    else:
        print(f"发送验证码到 {phone}...")
        await client.send_code_request(phone)
        print("验证码已发送！请查看 Telegram 收到的验证码")
        print(f"然后运行: python3 {SKILL_DIR}/scripts/login_step2.py <验证码>")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(send_code())
