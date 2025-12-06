import sys
import asyncio
import importlib
from flask import Flask
import threading
import config
from ROCKY import ID_CHATBOT
from pyrogram import idle
from pyrogram.types import BotCommand
from config import OWNER_ID
from ROCKY import LOGGER, ROCKY, userbot, load_clone_owners
from ROCKY.modules import ALL_MODULES
from ROCKY.modules.Clone import restart_bots
from ROCKY.modules.Id_Clone import restart_idchatbots

async def anony_boot():
    try:
        await ROCKY.start()
        try:
            await ROCKY.send_message(int(OWNER_ID), f"**{ROCKY.mention} Is started✅**")
        except Exception as ex:
            LOGGER.info(f"@{ROCKY.username} Started, please start the bot from owner id.")
    
        asyncio.create_task(restart_bots())
        asyncio.create_task(restart_idchatbots())
        await load_clone_owners()

        if config.STRING1:
            try:
                await userbot.start()
                try:
                    await ROCKY.send_message(int(OWNER_ID), "**Id-Chatbot Also Started✅**")
                except:
                    LOGGER.info("Id chatbot started but message failed.")
            except Exception as ex:
                print(f"Error in id-chatbot :- {ex}")
                pass

    except Exception as ex:
        LOGGER.error(ex)

    for all_module in ALL_MODULES:
        importlib.import_module("ROCKY.modules." + all_module)
        LOGGER.info(f"Successfully imported : {all_module}")

    try:
        await ROCKY.set_bot_commands(
            commands=[
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Bot help menu"),
                BotCommand("clone", "Make chatbot"),
                BotCommand("idclone", "Make id chatbot"),
            ]
        )
        LOGGER.info("Bot commands set successfully.")
    except Exception as ex:
        LOGGER.error(f"Failed to set bot commands: {ex}")

    LOGGER.info(f"@{ROCKY.username} Started.")

    await asyncio.Event().wait()


app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # ✔ FIXED — Event loop create first
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(anony_boot())
    finally:
        loop.close()
