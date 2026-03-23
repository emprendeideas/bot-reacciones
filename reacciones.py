import random
import asyncio
import os
import sys
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

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

EMOJIS = ["👍","🔥","💯","😎","🤝","👏"]

client1 = TelegramClient(StringSession(SESSION_1), API_ID, API_HASH)
client2 = TelegramClient(StringSession(SESSION_2), API_ID, API_HASH)
client3 = TelegramClient(StringSession(SESSION_3), API_ID, API_HASH)


async def reaccionar(client, nombre):
    print(f"{nombre} activo", flush=True)
    sys.stdout.flush()

    mensajes_procesados = set()

    while True:
        try:
            for canal in CHANNELS:
                async for msg in client.iter_messages(canal, limit=5):

                    # evitar repetir mensajes
                    if msg.id in mensajes_procesados:
                        continue

                    if msg.text is None:
                        continue

                    mensajes_procesados.add(msg.id)

                    emoji = random.choice(EMOJIS)

                    # delay más humano
                    delay = random.randint(20, 60)
                    print(f"{nombre} esperando {delay}s", flush=True)
                    await asyncio.sleep(delay)

                    await client(functions.messages.SendReactionRequest(
                        peer=msg.chat_id,
                        msg_id=msg.id,
                        reaction=[types.ReactionEmoji(emoji)]
                    ))

                    print(f"{nombre} reaccionó en {canal}: {emoji}", flush=True)

            # limpiar memoria si crece mucho
            if len(mensajes_procesados) > 5000:
                mensajes_procesados.clear()

            await asyncio.sleep(10)

        except Exception as e:
            print(f"Error en {nombre}: {e}", flush=True)
            await asyncio.sleep(10)


async def main():
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
