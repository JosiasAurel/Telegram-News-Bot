from telethon.client import TelegramClient
import json
import requests
from fastapi import FastAPI

app = FastAPI()

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"

# time to play around with Hacker News weird API
def fetch_posts():
    top_stories = requests.get(f"{HN_BASE_URL}/topstories.json").json()

    latest_articles = []

    for count, id_ in enumerate(top_stories):
        if count == 20:
            break
        article = requests.get(f"{HN_BASE_URL}/item/{id_}.json").json()
        latest_articles.append(article)

    return latest_articles


with open("config.json", "r") as config_json:
    json_content = json.loads(config_json.read())

api_id = json_content.get("api_id")
api_hash = json_content.get("api_hash")

@app.get("/")
async def _root():
    async with TelegramClient("name", api_id, api_hash) as client:
        posts = fetch_posts()
        # time to send all those messages
        await client.send_message(
            "me", "Good morning, Master. \nHere is your daily dose of Hacker News"
        )
        for post in posts:
            message = f"""
				{post.get("title")}            
				Posted by {post.get("by")}
				More -> {post.get("url")}
				"""
            await client.send_message("me", message)

    await client.send_message("me", "That's it for today.")
    return "Sending juice your way"

