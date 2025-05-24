import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import *
from helper_func import encode, admin

@Bot.on_message(filters.private & admin & ~filters.command(['start', 'commands','users','broadcast','batch', 'custom_batch', 'genlink','stats', 'dlt_time', 'check_dlt_time', 'dbroadcast', 'ban', 'unban', 'banlist', 'addchnl', 'delchnl', 'listchnl', 'fsub_mode', 'pbroadcast', 'add_admin', 'deladmin', 'admins', 'ping', 'logs', 'restart']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    
    # Check if message has content before copying
    if not (message.text or message.media or message.caption or message.sticker or message.animation or message.document or message.photo or message.video or message.audio or message.voice or message.video_note):
        await reply_text.edit_text("Cannot process empty message!")
        return
    
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        try:
            post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
        except Exception as retry_error:
            print(f"Retry failed: {retry_error}")
            await reply_text.edit_text("Failed to process message after retry!")
            return
    except Exception as e:
        print(f"Copy error: {e}")
        if "Empty messages cannot be copied" in str(e):
            await reply_text.edit_text("Cannot process empty message!")
        else:
            await reply_text.edit_text("Something went Wrong..!")
        return
    
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)