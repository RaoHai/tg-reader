#!/usr/bin/env python3
"""
TG Reader - 用 Telethon 读取 Telegram 群消息
可以看到 bot 消息！
"""

import asyncio
import argparse
import json
import os
from pathlib import Path

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
SESSION_DIR = SKILL_DIR / "sessions"


def load_config():
    if not CONFIG_FILE.exists():
        print(f"错误：配置文件不存在 {CONFIG_FILE}")
        print("请创建配置文件，包含 api_id 和 api_hash")
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)


async def read_messages(limit: int = 50):
    config = load_config()
    if not config:
        return

    api_id = int(config["api_id"])
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "tg_session")
    chat_id = config.get("chat_id")  # 从配置读取群组ID

    if not chat_id:
        print("错误：需要在 config.json 中设置 chat_id")
        return

    # session 文件放在 sessions 目录
    session_path = SESSION_DIR / session_name

    client = TelegramClient(str(session_path), api_id, api_hash)

    await client.connect()

    # 检查是否已登录
    if not await client.is_user_authorized():
        print("错误：未登录！请先运行 login.py 完成登录")
        await client.disconnect()
        return

    try:
        # 先解析 entity，避免 PeerIdInvalidError
        entity = await client.get_entity(chat_id)
        messages = await client.get_messages(entity, limit=limit)

        print(f"\n=== 最近 {len(messages)} 条消息 ===\n")

        for msg in reversed(messages):
            if msg.text:
                sender = "Unknown"
                if msg.sender:
                    if hasattr(msg.sender, 'first_name'):
                        sender = msg.sender.first_name or ""
                        if hasattr(msg.sender, 'last_name') and msg.sender.last_name:
                            sender += f" {msg.sender.last_name}"
                    elif hasattr(msg.sender, 'title'):
                        sender = msg.sender.title
                    
                    # 标记 bot
                    if hasattr(msg.sender, 'bot') and msg.sender.bot:
                        sender = f"[BOT] {sender}"

                time_str = msg.date.strftime("%m-%d %H:%M")
                print(f"[{time_str}] {sender}: {msg.text[:200]}")
                print()
    finally:
        await client.disconnect()


def main():
    parser = argparse.ArgumentParser(description="读取 Telegram 群消息")
    parser.add_argument("--limit", type=int, default=50, help="消息数量")

    args = parser.parse_args()

    asyncio.run(read_messages(args.limit))


if __name__ == "__main__":
    main()
