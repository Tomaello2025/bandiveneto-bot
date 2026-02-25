import requests
from bs4 import BeautifulSoup
import json
import os
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHANNEL_ID = "@bandiveneto_bot"

URL = "https://bandi.regione.veneto.it/Public/Elenco?Tipo=1"

bot = Bot(token=TOKEN)

def get_bandi():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    bandi = []

    for row in soup.select("table tbody tr"):
        titolo = row.select_one("td:nth-child(1)").text.strip()
        link = row.select_one("a")["href"]
        bandi.append((titolo, link))

    return bandi

def load_old():
    try:
        with open("bandi.json") as f:
            return json.load(f)
    except:
        return []

def save_new(bandi):
    with open("bandi.json", "w") as f:
        json.dump(bandi, f)

def main():
    vecchi = load_old()
    nuovi = get_bandi()

    for b in nuovi:
        if b not in vecchi:
            msg = f"📢 Nuovo bando!\n\n{b[0]}\n🔗 https://bandi.regione.veneto.it{b[1]}"
            bot.send_message(chat_id=CHANNEL_ID, text=msg)

    save_new(nuovi)

main()
