# from django.conf import settings
import requests
import asyncio
from .models import TelegramClients
import os
BASE_URL = "https://api.telegram.org/bot"

async def _make_request(url,data):
    requests.post(
        url, 
        data=data,
        timeout=5000
    )


def sendTelegramMessage(body,sender_name,sender_phone, sender_email, header="New Query Form Filled"):
    clients = TelegramClients.all()
    if not clients:return False

    MESSAGE_TEMPLATE =f"""
*{header}*

{body}

Sender Details
{sender_name}
```{sender_email}```
{sender_phone}
    """
    try:
        action = "sendMessage"
        # url = "https://api.telegram.org/bot<token>/sendMessage"
        url = BASE_URL + os.environ['TELEGRAM_BOT_KEY'] + "/" + action
        data = {
            "text": MESSAGE_TEMPLATE,
            "parse_mode": "MarkdownV2",
        }
        for client in clients:
            data["chat_id"] = client.chat_id
            asyncio.run(_make_request(url, data))
    except Exception as e:
        print(e)