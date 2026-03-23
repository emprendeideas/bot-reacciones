import random
import asyncio
import os
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
    print(f"{nombre} activo")

    while True:
        try:
            for canal in CHANNELS:
                async for msg in client.iter_messages(canal, limit=3):

                    if msg.text is None:
                        continue

                    emoji = random.choice(EMOJIS)

                    await asyncio.sleep(random.randint(15, 40))

                    await client(functions.messages.SendReactionRequest(
                        peer=msg.chat_id,
                        msg_id=msg.id,
                        reaction=[types.ReactionEmoji(emoji)]
                    ))

                    print(f"{nombre} reaccionó en {canal}: {emoji}")

            await asyncio.sleep(10)

        except Exception as e:
            print(f"Error en {nombre}: {e}")
            await asyncio.sleep(10)


async def main():
    await client1.connect()
    await client2.connect()
    await client3.connect()

    await asyncio.gather(
        reaccionar(client1, "Cuenta 1"),
        reaccionar(client2, "Cuenta 2"),
        reaccionar(client3, "Cuenta 3")
    )


asyncio.run(main())