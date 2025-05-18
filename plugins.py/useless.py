
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

# NEW COMMANDS FOR IMAGE AND SHORTENER MANAGEMENT

@Bot.on_message(filters.command('addforcepic') & filters.private & admin)  
async def add_force_pics(client: Bot, message: Message):
    logger.debug(f"Received /addforcepic command from user {message.from_user.id}")
    if len(message.command) != 2:
        await message.reply("<b>Usage:</b> <code>/addforcepic [image_url]</code>")
        return
    url = message.command[1]
    # Basic URL validation
    if not url.startswith("http"):
        await message.reply("<b>Invalid URL. Please provide a valid image URL starting with http or https.</b>")
        return
    try:
        await db.add_force_pics(url)  # Removed added_by parameter
        await message.reply(f"<b>Force Sub Picture added:</b> <code>{url}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to add Force Sub Picture:</b> <code>{str(e)}</code>")

# Add Start Sub Picture
@Bot.on_message(filters.command('addstartpic') & filters.private & admin)
async def add_start_sub_pic(client: Bot, message: Message):
    logger.debug(f"Received /addstartpic command from user {message.from_user.id}")
    if len(message.command) != 2:
        await message.reply("<b>Usage:</b> <code>/addstartpic [image_url]</code>")
        return
    url = message.command[1]
    if not url.startswith("http"):
        await message.reply("<b>Invalid URL. Please provide a valid image URL starting with http or https.</b>")
        return
    try:
        await db.add_start_pics(url)  # Removed added_by parameter
        await message.reply(f"<b>Start Sub Picture added:</b> <code>{url}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to add Start Sub Picture:</b> <code>{str(e)}</code>")

# Delete Force Sub Picture
@Bot.on_message(filters.command('delforcepic') & filters.private & admin)  
async def del_force_pics(client: Bot, message: Message):
    logger.debug(f"Received /delforcepic command from user {message.from_user.id}")
    if len(message.command) != 2:
        await message.reply("<b>Usage:</b> <code>/delforcepic [photo_id]</code>\nUse /showforcepic to get the photo_id.")
        return
    photo_id = message.command[1]
    try:
        await db.delete_force_pics(photo_id)
        await message.reply(f"<b>Force Sub Picture deleted:</b> <code>{photo_id}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to delete Force Sub Picture:</b> <code>{str(e)}</code>")

# Delete Start Sub Picture
@Bot.on_message(filters.command('delstartpic') & filters.private & admin)  
async def del_start_pic(client: Bot, message: Message):
    logger.debug(f"Received /delstartpic command from user {message.from_user.id}")
    if len(message.command) != 2:
        await message.reply("<b>Usage:</b> <code>/delstartpic [photo_id]</code>\nUse /showstartpic to get the photo_id.")
        return
    photo_id = message.command[1]
    try:
        await db.delete_start_pics(photo_id)
        await message.reply(f"<b>Start Sub Picture deleted:</b> <code>{photo_id}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to delete Start Sub Picture:</b> <code>{str(e)}</code>")

# Show All Force Sub Pictures
@Bot.on_message(filters.command('showforcepic') & filters.private & admin)  
async def show_force_pics(client: Bot, message: Message):
    logger.debug(f"Received /showforcepic command from user {message.from_user.id}")
    try:
        pics = await db.get_force_pics()
        if not pics:
            await message.reply("<b>No Force Sub Pictures found.</b>")
            return
        pic_list = "\n".join([f"ID: <code>{str(pic['_id'])}</code>\nURL: <code>{pic['url']}</code>" for pic in pics])
        await message.reply(f"<b>Force Sub Pictures:</b>\n{pic_list}")
    except Exception as e:
        await message.reply(f"<b>Failed to fetch Force Sub Pictures:</b> <code>{str(e)}</code>")

# Show All Start Sub Pictures
@Bot.on_message(filters.command('showstartpic') & filters.private & admin)  
async def show_start_sub_pics(client: Bot, message: Message):
    logger.debug(f"Received /showstartpic command from user {message.from_user.id}")
    try:
        pics = await db.get_start_pics()
        if not pics:
            await message.reply("<b>No Start Sub Pictures found.</b>")
            return
        pic_list = "\n".join([f"ID: <code>{str(pic['_id'])}</code>\nURL: <code>{pic['url']}</code>" for pic in pics])
        await message.reply(f"<b>Start Sub Pictures:</b>\n{pic_list}")
    except Exception as e:
        await message.reply(f"<b>Failed to fetch Start Sub Pictures:</b> <code>{str(e)}</code>")

# Edit Shortener Settings
@Bot.on_message(filters.command('shortner') & filters.private & admin)
async def edit_shortner(client: Bot, message: Message):
    logger.debug(f"Received /shortner command from user {message.from_user.id}")
    if len(message.command) != 3:
        await message.reply("<b>Usage:</b> <code>/shortner [new_shortlink_url] [new_shortlink_api]</code>")
        return
    new_url = message.command[1]
    new_api = message.command[2]
    if not new_url.startswith("http"):
        await message.reply("<b>Invalid Shortlink URL. Please provide a valid URL starting with http or https.</b>")
        return
    try:
        # Update the SHORTLINK_URL and SHORTLINK_API environment variables at runtime
        os.environ['SHORTLINK_URL'] = new_url
        os.environ['SHORTLINK_API'] = new_api

        # Update the .env file
        env_file = find_dotenv()
        if env_file:
            with open(env_file, 'r') as file:
                lines = file.readlines()
            with open(env_file, 'w') as file:
                found_url = False
                found_api = False
                for line in lines:
                    if line.startswith("SHORTLINK_URL="):
                        file.write(f"SHORTLINK_URL={new_url}\n")
                        found_url = True
                    elif line.startswith("SHORTLINK_API="):
                        file.write(f"SHORTLINK_API={new_api}\n")
                        found_api = True
                    else:
                        file.write(line)
                if not found_url:
                    file.write(f"SHORTLINK_URL={new_url}\n")
                if not found_api:
                    file.write(f"SHORTLINK_API={new_api}\n")

        await message.reply(f"<b>Shortlink updated:</b>\nURL: <code>{new_url}</code>\nAPI: <code>{new_api}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to update Shortlink:</b> <code>{str(e)}</code>")

@Bot.on_message(filters.command('edittutvid') & filters.private & admin)
async def edit_tut_vid(client: Bot, message: Message):
    logger.debug(f"Received /edittutvid command from user {message.from_user.id}")
    if len(message.command) != 2:
        await message.reply("<b>Usage:</b> <code>/edittutvid [new_tutorial_url]</code>")
        return
    new_url = message.command[1]
    if not new_url.startswith("http"):
        await message.reply("<b>Invalid URL. Please provide a valid URL starting with http or https.</b>")
        return
    try:
        # Update the TUT_VID environment variable at runtime
        os.environ['TUT_VID'] = new_url

        # Update the .env file
        env_file = find_dotenv()
        if env_file:
            with open(env_file, 'r') as file:
                lines = file.readlines()
            with open(env_file, 'w') as file:
                found = False
                for line in lines:
                    if line.startswith("TUT_VID="):
                        file.write(f"TUT_VID={new_url}\n")
                        found = True
                    else:
                        file.write(line)
                if not found:
                    file.write(f"TUT_VID={new_url}\n")

        await message.reply(f"<b>Tutorial Video URL updated to:</b> <code>{new_url}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to update Tutorial Video URL:</b> <code>{str(e)}</code>")

# Show Current Shortener Settings
@Bot.on_message(filters.command('showshortner') & filters.private & admin)
async def show_shortner(client: Bot, message: Message):
    logger.debug(f"Received /showshortner command from user {message.from_user.id}")
    try:
        current_api = SHORTLINK_API
        current_url = SHORTLINK_URL
        await message.reply(f"<b>Current Shortener Settings:</b>\nSHORTLINK_API: <code>{current_api}</code>\nSHORTLINK_URL: <code>{current_url}</code>")
    except Exception as e:
        await message.reply(f"<b>Failed to fetch shortener settings:</b> <code>{str(e)}</code>")
