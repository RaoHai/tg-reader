# TG Reader 🐕

用 Telethon 读取 Telegram 群消息，**包括 bot 消息**！

这是小狗🐕机器人的 skill，由 CC 老师帮忙重写，小狗用 skill-creator 重构。

## 为什么需要这个？

Telegram Bot API 有个限制：bot 看不到其他 bot 的消息。

但用 Telethon（用户 API）就可以！登录后能看到群里所有消息。

## 快速开始

### 1. 安装依赖

```bash
pip install telethon
```

### 2. 获取 API 凭证

1. 访问 https://my.telegram.org
2. 用手机号登录
3. 点 "API development tools"
4. 创建 App，获取 `api_id` 和 `api_hash`

### 3. 配置

编辑 `config.json`：

```json
{
  "api_id": "你的api_id",
  "api_hash": "你的api_hash",
  "session_name": "tg_session",
  "phone": "+86手机号",
  "password": "两步验证密码(可选)",
  "chat_id": -5202820098
}
```

### 4. 登录

```bash
# 发送验证码
python3 scripts/login.py

# 输入验证码完成登录
python3 scripts/login_step2.py <验证码>

# 如果有两步验证
python3 scripts/login_step2.py <验证码> <密码>
```

### 5. 使用

```bash
# 读取最近 100 条消息
python3 scripts/reader.py --limit 100

# 列出所有对话和 ID
python3 scripts/list_chats.py
```

## 文件结构

```
tg-reader/
├── SKILL.md          # Skill 描述（给 AI 看的）
├── README.md         # 使用说明（给人看的）
├── config.json       # 配置文件（不要提交！）
├── scripts/
│   ├── login.py      # 登录步骤1：发验证码
│   ├── login_step2.py # 登录步骤2：输入验证码
│   ├── reader.py     # 读取消息
│   └── list_chats.py # 列出对话
└── sessions/         # Session 文件（不要提交！）
```

## 注意事项

- `config.json` 和 `sessions/` 包含敏感信息，已在 `.gitignore` 中
- 首次登录需要手机验证码
- Session 有效期很长，不用每次都登录

汪！🐕
