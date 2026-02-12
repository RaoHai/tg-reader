#!/usr/bin/env python3
"""
Telethon 登录脚本 - 步骤2：输入验证码完成登录
用法: python3 login_step2.py <验证码> [两步验证密码]
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
SESSION_DIR = SKILL_DIR / "sessions"


def load_config():
    if not CONFIG_FILE.exists():
        print(f"错误：配置文件不存在 {CONFIG_FILE}")
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)


async def sign_in(code: str, password: str = None):
    config = load_config()
    if not config:
        return

    api_id = int(config["api_id"])
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "tg_session")
    phone = config.get("phone") or os.getenv("TG_PHONE")

    if not password:
        password = config.get("password") or os.getenv("TG_PASSWORD")

    if not phone:
        print("错误：需要在 config.json 中设置 phone 或设置环境变量 TG_PHONE")
        return

    SESSION_DIR.mkdir(exist_ok=True)
    session_path = SESSION_DIR / session_name

    client = TelegramClient(str(session_path), api_id, api_hash)
    await client.connect()

    try:
        await client.sign_in(phone, code)
        print("登录成功！")
    except SessionPasswordNeededError:
        if not password:
            print("错误：需要两步验证密码")
            print("请在 config.json 中设置 password 或设置环境变量 TG_PASSWORD")
            print("或者运行: python3 login_step2.py <验证码> <密码>")
            await client.disconnect()
            return

        await client.sign_in(password=password)
        print("登录成功！")

    me = await client.get_me()
    print(f"当前账号: {me.first_name} (@{me.username})")

    await client.disconnect()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 login_step2.py <验证码> [两步验证密码]")
        sys.exit(1)

    code = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None

    asyncio.run(sign_in(code, password))
