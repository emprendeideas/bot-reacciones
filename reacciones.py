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

EMOJIS_HABILITADOS = [
    "👍", "❤", "🔥", "🥰", "👏", "🐳", "🤯", "😱", "🎉", "🤩",
    "🙏", "👌", "😍", "❤‍🔥", "💯", "🏆", "🍾", "🤓", "🤝", "😘", "😎"
]

client1 = TelegramClient(StringSession(SESSION_1), API_ID, API_HASH)
client2 = TelegramClient(StringSession(SESSION_2), API_ID, API_HASH)
client3 = TelegramClient(StringSession(SESSION_3), API_ID, API_HASH)


async def reaccionar(client, nombre):
    ultimo_id_por_canal = {}
    nombres_canales = {}
    mensajes_procesados = set()

    print(f"🤖 {nombre} LISTO", flush=True)

    # 🔥 inicialización EXACTA del original
    for canal in CHANNELS:
        entity = await client.get_entity(canal)
        nombres_canales[canal] = entity.title if hasattr(entity, "title") else "Canal"

        async for msg in client.iter_messages(canal, limit=1):
            ultimo_id_por_canal[canal] = msg.id

        print(f"{nombre} monitorea {nombres_canales[canal]}", flush=True)

    while True:
        try:
            for canal in CHANNELS:

                async for msg in client.iter_messages(
                    canal,
                    min_id=ultimo_id_por_canal.get(canal, 0)
                ):

                    # 🔥 MISMAS VALIDACIONES
                    if msg.id in mensajes_procesados:
                        continue

                    if msg.action is not None or msg.text is None:
                        continue

                    mensajes_procesados.add(msg.id)

                    ultimo_id_por_canal[canal] = max(
                        ultimo_id_por_canal.get(canal, 0),
                        msg.id
                    )

                    canal_nombre = nombres_canales[canal]

                    print(f"📩 [{nombre}] Nuevo mensaje en {canal_nombre}: {msg.id}", flush=True)

                    # 🔥 MISMA LÓGICA ORIGINAL
                    if nombre in ["Cuenta 2", "Cuenta 3"]:
                        num_reacciones = 1
                    else:
                        num_reacciones = random.randint(1, 3)

                    emojis = random.sample(EMOJIS_HABILITADOS, num_reacciones)

                    print(f"{nombre} enviará {num_reacciones} reacciones", flush=True)

                    for emoji in emojis:
                        await asyncio.sleep(60)

                    try:
                        await client(functions.messages.SendReactionRequest(
                            peer=msg.chat_id,
                            msg_id=msg.id,
                            big=False,
                            add_to_recent=True,
                            reaction=[types.ReactionEmoji(e) for e in emojis]
                        ))

                        print(f"{nombre} reaccionó con {emojis}", flush=True)

                        await asyncio.sleep(random.uniform(2, 5))

                    except Exception as e:
                        print(f"Error en {nombre}: {e}", flush=True)

            if len(mensajes_procesados) > 5000:
                mensajes_procesados.clear()

            await asyncio.sleep(5)

        except Exception as e:
            print(f"Error general {nombre}: {e}", flush=True)
            await asyncio.sleep(10)


async def main():
    iniciar_web()

    await client1.start()
    await client2.start()
    await client3.start()

    print("🔥 3 CUENTAS INICIADAS", flush=True)

    await asyncio.gather(
        reaccionar(client1, "Cuenta 1"),
        reaccionar(client2, "Cuenta 2"),
        reaccionar(client3, "Cuenta 3")
    )


asyncio.run(main())
