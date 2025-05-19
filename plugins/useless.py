
import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from dotenv import *

# Debug logging setup
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SHORTLINK_API = os.environ.get("SHORTLINK_API", "573350da0e10a5a44f7e6fec3bc2b3f836b47805")  # Default Shortlink API
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "linkshortify.com")  # Default Shortlink URL

#=====================================================================================##

@Bot.on_message(filters.command('stats') & filters.private & admin)
async def stats(bot: Bot, message: Message):
    logger.debug(f"Received /stats command from user {message.from_user.id}")
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"

#=====================================================================================##

@Bot.on_message(filters.command('users') & filters.private & admin)
async def get_users(client: Bot, message: Message):
    logger.debug(f"Received /users command from user {message.from_user.id}")
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

#=====================================================================================##

# AUTO-DELETE

@Bot.on_message(filters.private & filters.command('dlt_time') & admin)
async def set_delete_time(client: Bot, message: Message):
    logger.debug(f"Received /dlt_time command from user {message.from_user.id}")
    try:
        duration = int(message.command[1])
        await db.set_del_timer(duration)
        await message.reply(f"<b>Dᴇʟᴇᴛᴇ Tɪᴍᴇʀ ʜᴀs ʙᴇᴇɴ sᴇᴛ ᴛᴏ <blockquote>{duration} sᴇᴄᴏɴᴅs.</blockquote></b>")
    except (IndexError, ValueError):
        await message.reply("<b>Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs.</b> Usage: /dlt_time {duration}")

@Bot.on_message(filters.private & filters.command('check_dlt_time') & admin)
async def check_delete_time(client: Bot, message: Message):
    logger.debug(f"Received /check_dlt_time command from user {message.from_user.id}")
    duration = await db.get_del_timer()
    await message.reply(f"<b><blockquote>Cᴜʀʀᴇɴᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ ɪs sᴇᴛ ᴛᴏ {duration}sᴇᴄᴏɴᴅs.</blockquote></b>")

#=====================================================================================##

# NEW COMMANDS FROM PREVIOUS UPDATE

# Ping command to check bot's response time
@Bot.on_message(filters.private & filters.command('ping') & admin)
async def ping_bot(client: Bot, message: Message):
    logger.debug(f"Received /ping command from user {message.from_user.id}")
    start_time = time.time()
    msg = await message.reply("<b>Pinging...</b>")
    end_time = time.time()
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    await msg.edit(f"<b><blockquote>Cᴜʀʀᴇɴᴛ Lᴀᴛᴇɴᴄʏ ɪs {latency:.2f}ᴍɪʟʟɪ sᴇᴄᴏɴᴅs.</blockquote></b>")

# <b>Pong!</b> Latency: <code>{latency:.2f} ms</code>


# Logs command to fetch recent logs (admin-only)
@Bot.on_message(filters.command('logs') & filters.private & admin)
async def get_logs(client: Bot, message: Message):
    logger.debug(f"Received /logs command from user {message.from_user.id}")
    try:
        num_lines = 50  # Number of lines to fetch
        if len(message.command) > 1:
            try:
                num_lines = int(message.command[1])
                if num_lines <= 0:
                    raise ValueError
            except ValueError:
                await message.reply("<b>Please provide a valid number of lines.</b> Usage: /logs [number]")
                return

        # Read the last `num_lines` from the log file
        with open(LOG_FILE_NAME, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-num_lines:] if len(lines) >= num_lines else lines
            log_content = "".join(last_lines)

        if not log_content.strip():
            await message.reply("<b>No logs found.</b>")
            return

        # Send logs as a message (if too long, split into multiple messages)
        if len(log_content) > 4096:  # Telegram message length limit
            for i in range(0, len(log_content), 4096):
                await message.reply(f"<code>{log_content[i:i+4096]}</code>")
        else:
            await message.reply(f"<b>Recent Logs:</b>\n<code>{log_content}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to fetch logs:</b> <code>{str(e)}</code>")

# Restart command (admin-only)
@Bot.on_message(filters.command('restart') & filters.private & admin)
async def restart_bot(client: Bot, message: Message):
    logger.debug(f"Received /restart command from user {message.from_user.id}")
    msg = await message.reply("<b>Restarting bot...</b>")
    try:
        # Notify the owner
        await client.send_message(OWNER_ID, "<b>Bot is restarting...</b>")
        # Log the restart
        LOGGER(__name__).info("Bot is restarting...")
        # Stop the bot gracefully
        await client.stop()
        # Restart the process (this works if the bot is run with a process manager like PM2 or Heroku)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        await msg.edit(f"<b>Failed to restart:</b> <code>{str(e)}</code>")

#=====================================================================================##