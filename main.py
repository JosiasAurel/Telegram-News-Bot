from telethon.sync import TelegramClient
import json


with open("config.json", "r") as config_json:
    json_content = json.loads(config_json.read())

api_id = json_content.get("api_id")
api_hash = json_content.get("api_hash")

with TelegramClient("name", api_id, api_hash) as client:
    client.send_message("me", "I love you Josias")

    client.run_until_disconnected()
