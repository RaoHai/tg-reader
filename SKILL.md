# TG Reader

读取 Telegram 群消息（包括 bot 消息）

使用 Telethon 以用户身份访问 Telegram，可以看到所有消息包括 bot 消息。

## 配置

复制配置文件模板：

```bash
cp config.json.example config.json
```

编辑 `config.json`：

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

获取 `api_id` 和 `api_hash`：访问 https://my.telegram.org

或使用环境变量：`TG_PHONE`, `TG_PASSWORD`

## 首次登录

```bash
# 步骤1：发送验证码
python3 login.py

# 步骤2：输入验证码完成登录
python3 login_step2.py <验证码>

# 如果有两步验证
python3 login_step2.py <验证码> <密码>
```

## 使用

先用 `list_chats.py` 找到群组 ID，然后在 `config.json` 中设置 `chat_id`。

运行：

```bash
# 读取最近 100 条消息
python3 reader.py --limit 100

# 默认 50 条
python3 reader.py
```

## 工具

```bash
# 列出所有对话和 ID
python3 list_chats.py
```

## 依赖

```bash
pip install telethon
```
