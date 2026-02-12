#!/usr/bin/env python3
"""
列出所有 Telegram 对话（群组、频道、私聊）及其 ID
"""

import asyncio
import json
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


async def list_chats():
    config = load_config()
    if not config:
        return

    api_id = int(config["api_id"])
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "nanobot_reader")
    session_path = SESSION_DIR / session_name

    client = TelegramClient(str(session_path), api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        print("错误：未登录！请先运行 login.py")
        await client.disconnect()
        return

    try:
        print("\n=== 你的所有对话 ===\n")

        async for dialog in client.iter_dialogs():
            entity = dialog.entity

            # 判断类型
            if hasattr(entity, 'megagroup') and entity.megagroup:
                chat_type = "超级群组"
            elif hasattr(entity, 'broadcast') and entity.broadcast:
                chat_type = "频道"
            elif hasattr(entity, 'username'):
                chat_type = "群组/私聊"
            else:
                chat_type = "私聊"

            # 获取名称
            name = getattr(entity, 'title', None) or getattr(entity, 'first_name', 'Unknown')

            print(f"[{chat_type}] {name}")
            print(f"  ID: {dialog.id}")
            print()

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(list_chats())
