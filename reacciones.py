import random
import asyncio
import os
import threading
from flask import Flask

from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

# 🔥 SERVIDOR PARA RENDER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def iniciar_web():
    t = threading.Thread(target=run_web)
    t.start()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

SESSION_1 = os.getenv("SESSION_1")
SESSION_2 = os.getenv("SESSION_2")
SESSION_3 = os.getenv("SESSION_3")

CHANNELS = [
    -1001766759604,
    -1002104468392,
    -1001908992418,
    -1002713454932,
    -1003151989995
]

EMOJIS = ["👍", "❤", "🔥", "🥰", "👏", "🐳", "🤯", "😱", "🎉", "🤩",
    "🙏", "👌", "😍", "💯", "🏆", "🍾", "🤓", "🤝", "😘", "😎"]

client1 = TelegramClient(StringSession(SESSION_1), API_ID, API_HASH)
client2 = TelegramClient(StringSession(SESSION_2), API_ID, API_HASH)
client3 = TelegramClient(StringSession(SESSION_3), API_ID, API_HASH)


async def reaccionar(client, nombre):
    ultimo_id_por_canal = {}
    print(f"{nombre} activo", flush=True)

    # 🔥 obtener último mensaje actual (punto de inicio)
    for canal in CHANNELS:
        async for msg in client.iter_messages(canal, limit=1):
            ultimo_id_por_canal[canal] = msg.id

    while True:
        try:
            for canal in CHANNELS:

                async for msg in client.iter_messages(
                    canal,
                    min_id=ultimo_id_por_canal.get(canal, 0)
                ):

                    if msg.text is None:
                        continue

                    # actualizar último id
                    ultimo_id_por_canal[canal] = msg.id

                    emoji = random.choice(EMOJIS)

                    delay = random.randint(20, 60)
                    print(f"{nombre} esperando {delay}s", flush=True)
                    await asyncio.sleep(delay)

                    await client(functions.messages.SendReactionRequest(
                        peer=msg.chat_id,
                        msg_id=msg.id,
                        reaction=[types.ReactionEmoji(emoji)]
                    ))

                    print(f"{nombre} reaccionó en {canal}: {emoji}", flush=True)

            await asyncio.sleep(5)

        except Exception as e:
            print(f"Error en {nombre}: {e}", flush=True)
            await asyncio.sleep(10)


async def main():
    iniciar_web()

    await client1.connect()
    await client2.connect()
    await client3.connect()

    print("🔥 BOT INICIADO CORRECTAMENTE", flush=True)

    await asyncio.gather(
        reaccionar(client1, "Cuenta 1"),
        reaccionar(client2, "Cuenta 2"),
        reaccionar(client3, "Cuenta 3")
    )


asyncio.run(main())
