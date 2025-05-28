import asyncio
import os
import random
import sys
import re
import string 
import string as rohit
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
from database.db_premium import *

BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    id = message.from_user.id

    # is_premium = await is_premium_user(id) {Not sure will this harm the bot or not}

    # Check if user is banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<b>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]]
            )
        )

    # ✅ Check Force Subscription
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    # File auto-delete time in seconds
    FILE_AUTO_DELETE = await db.get_del_timer()

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass



        start_pic = START_PIC  

    # Handle normal message flow
    text = message.text

    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]
            if basic.startswith("yu3elk"):
                base64_string = basic[6:-1]
            else:
                base64_string = basic

            if not is_premium and user_id != OWNER_ID and not basic.startswith("yu3elk"):
                await short_url(client, message, base64_string)
                return

        except Exception as e:
            print(f"Error processing start payload: {e}")

        string = await decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        try:
            temp_msg = await message.reply("<b>Please wait...</b>")
        except Exception as e:
            if "USER_IS_BLOCKED" in str(e):
                print(f"User {message.from_user.id} has blocked the bot")
                return
            else:
                print(f"Error sending temp message: {e}")
                return
                
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            try:
                await message.reply_text("Something went wrong!")
            except:
                print(f"User {message.from_user.id} has blocked the bot")
            print(f"Error getting messages: {e}")
            return
        finally:
            try:
                await temp_msg.delete()
            except:
                pass

        codeflix_msgs = []
        for msg in messages:
            # Check if message has content before copying
            if not (msg.text or msg.media or msg.caption or msg.sticker or msg.animation or 
                   msg.document or msg.photo or msg.video or msg.audio or msg.voice or msg.video_note):
                print(f"Skipping empty message ID: {msg.id}")
                continue
                
            caption = (CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, 
                                             filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                       else ("" if not msg.caption else msg.caption.html))

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                try:
                    copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, 
                                                reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    codeflix_msgs.append(copied_msg)
                except Exception as retry_error:
                    print(f"Failed to send message after retry: {retry_error}")
                    continue
            except Exception as e:
                if "Empty messages cannot be copied" in str(e):
                    print(f"Skipping empty message ID: {msg.id}")
                elif "USER_IS_BLOCKED" in str(e):
                    print(f"User {message.from_user.id} has blocked the bot")
                    return
                else:
                    print(f"Failed to send message: {e}")
                continue

        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b>Tʜɪs Fɪʟᴇ ᴡɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ  {get_exp_time(FILE_AUTO_DELETE)}. Pʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ʙᴇғᴏʀᴇ ɪᴛ ɢᴇᴛs Dᴇʟᴇᴛᴇᴅ.</b>"
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in codeflix_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<b>ʏᴏᴜʀ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ ɪꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !!\n\nᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ 👇</b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("• ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs •", url="https://t.me/Infinix_Adult")],
                [
                    InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton('ʜᴇʟᴘ •', callback_data="help")
                ]
            ]
        )
        await message.reply_photo(
            photo=start_pic,  
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=5104841245755180586  # 🔥
        )
        return

#=====================================================================================#

# Create a global dictionary to store chat data
chat_data_cache = {}
invite_link_cache = {}  # Cache for storing persistent invite links

async def not_joined(client: Client, message: Message):
    """Ultra-optimized version with batch processing and persistent invite links"""
    user_id = message.from_user.id
    
    # Send checking subscription message
    temp_msg = await message.reply("<b><i>Checking Subscription...</i></b>")
    
    try:
        # Get all channels from database
        all_channels_data = await db.show_channels()
        
        if not all_channels_data:
            return
        
        # Handle different return formats from db.show_channels()
        channels_to_process = []
        
        # Check if the data is a list of tuples or just chat_ids
        for item in all_channels_data:
            if isinstance(item, tuple) and len(item) >= 2:
                # Data format: (chat_id, mode)
                chat_id, mode = item[0], item[1]
                channels_to_process.append((chat_id, mode))
            elif isinstance(item, (int, str)):
                # Data format: just chat_id, need to fetch mode separately
                chat_id = int(item)
                mode = await db.get_channel_mode(chat_id)
                channels_to_process.append((chat_id, mode))
            else:
                # Try to handle as dict or other format
                try:
                    if hasattr(item, 'get'):
                        chat_id = item.get('chat_id') or item.get('id')
                        mode = item.get('mode', 'off')
                    else:
                        chat_id = int(item)
                        mode = await db.get_channel_mode(chat_id)
                    channels_to_process.append((chat_id, mode))
                except Exception as e:
                    print(f"Error processing channel item {item}: {e}")
                    continue
        
        if not channels_to_process:
            return
        
        # Batch process subscription checks
        subscription_tasks = [
            is_sub(client, user_id, chat_id) 
            for chat_id, _ in channels_to_process
        ]
        
        subscription_results = await asyncio.gather(*subscription_tasks, return_exceptions=True)
        
        # Filter non-subscribed channels
        non_subscribed = [
            (chat_id, mode) for (chat_id, mode), is_subscribed in zip(channels_to_process, subscription_results)
            if not isinstance(is_subscribed, Exception) and not is_subscribed
        ]
        
        # If user is subscribed to all channels, delete temp message and return
        if not non_subscribed:
            await temp_msg.delete()
            return
        
        # Batch fetch chat data for non-subscribed channels
        chat_data_tasks = []
        for chat_id, mode in non_subscribed:
            if chat_id not in chat_data_cache:
                chat_data_tasks.append(client.get_chat(chat_id))
            else:
                chat_data_tasks.append(asyncio.create_task(async_return(chat_data_cache[chat_id])))
        
        chat_data_results = await asyncio.gather(*chat_data_tasks, return_exceptions=True)
        
        # Update cache and build buttons
        buttons = []
        for (chat_id, mode), chat_data in zip(non_subscribed, chat_data_results):
            if isinstance(chat_data, Exception):
                print(f"Error fetching chat data for {chat_id}: {chat_data}")
                continue
                
            # Update cache
            chat_data_cache[chat_id] = chat_data
            
            # Generate button with persistent invite link
            try:
                name = chat_data.title
                link = await get_or_create_invite_link(client, chat_id, mode, chat_data)
                buttons.append([InlineKeyboardButton(text=name, url=link)])
            except Exception as e:
                print(f"Error creating button for chat {chat_id}: {e}")
        
        # Add retry button
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except (IndexError, AttributeError):
            pass

        force_pic_url =  FORCE_PIC

        # Send final message
        await message.reply_photo(
            photo=force_pic_url,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        
        # Delete the temporary message after sending force sub message
        await temp_msg.delete()
        
    except Exception as e:
        print(f"Final Error in not_joined: {e}")
        await temp_msg.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Im_Sukuna02</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

async def get_or_create_invite_link(client: Client, chat_id: int, mode: str, chat_data):
    """
    Get existing invite link from cache or create a new persistent one
    """
    cache_key = f"{chat_id}_{mode}"
    
    # Check if we already have a cached invite link
    if cache_key in invite_link_cache:
        cached_link = invite_link_cache[cache_key]
        
        # Verify if the cached link is still valid
        if await is_invite_link_valid(client, chat_id, cached_link):
            return cached_link
        else:
            # Remove invalid link from cache
            del invite_link_cache[cache_key]
    
    # Create new invite link
    try:
        if chat_data.username:
            # For public channels, use the username link
            link = f"https://t.me/{chat_data.username}"
        else:
            # For private channels, create invite link
            if mode == "on":
                # Create join request link for "on" mode
                invite = await client.create_chat_invite_link(
                    chat_id=chat_id,
                    creates_join_request=True,
                    name=f"FSub_JoinRequest_{chat_id}",  # Named invite for easier management
                    # Remove expiry for persistent links
                )
            else:
                # Create regular invite link for other modes
                invite = await client.create_chat_invite_link(
                    chat_id=chat_id,
                    name=f"FSub_Regular_{chat_id}",  # Named invite for easier management
                    # Remove expiry for persistent links
                )
            
            link = invite.invite_link
        
        # Cache the new invite link
        invite_link_cache[cache_key] = link
        
        # Optional: Save to database for persistence across bot restarts
        await db.save_invite_link(chat_id, mode, link)
        
        return link
        
    except Exception as e:
        print(f"Error creating invite link for chat {chat_id}: {e}")
        # Fallback: return a basic invite if possible
        if chat_data.username:
            return f"https://t.me/{chat_data.username}"
        raise e

async def is_invite_link_valid(client: Client, chat_id: int, invite_link: str) -> bool:
    """
    Check if an invite link is still valid
    """
    try:
        # Extract invite hash from the link
        if "t.me/" in invite_link:
            if "+/" in invite_link or "joinchat/" in invite_link:
                # For invite links, try to get invite info
                invite_hash = invite_link.split("/")[-1]
                await client.get_chat_invite_link_info(invite_hash)
                return True
            else:
                # For username links, they don't expire
                return True
        return False
    except Exception:
        # If we can't verify or get an error, consider it invalid
        return False

async def async_return(value):
    """Helper function to return cached values as async tasks"""
    return value

# Initialize function that will be called from bot.py
async def initialize_invite_system():
    """
    Initialize the invite link system - load cached links from database
    """
    try:
        # Check if database has the required methods
        if hasattr(db, 'get_all_invite_links'):
            cached_links = await db.get_all_invite_links()
            for link_data in cached_links:
                try:
                    chat_id = link_data['chat_id']
                    mode = link_data['mode']
                    link = link_data['invite_link']
                    cache_key = f"{chat_id}_{mode}"
                    invite_link_cache[cache_key] = link
                except Exception as e:
                    print(f"Error loading cached link: {e}")
                    continue
            
            print(f"✅ Loaded {len(cached_links)} cached invite links")
        else:
            print("⚠️ Database doesn't support invite link caching - running without cache")
            
    except Exception as e:
        print(f"❌ Error initializing invite system: {e}")

async def cleanup_invalid_links():
    """
    Periodic cleanup function to remove invalid cached links
    """
    invalid_keys = []
    
    for cache_key, invite_link in invite_link_cache.items():
        try:
            # Basic validation - check if link format is correct
            if not invite_link or not invite_link.startswith("https://t.me/"):
                invalid_keys.append(cache_key)
        except Exception:
            invalid_keys.append(cache_key)
    
    # Remove invalid links
    for key in invalid_keys:
        del invite_link_cache[key]
        try:
            chat_id, mode = key.split("_", 1)
            if hasattr(db, 'delete_invite_link'):
                await db.delete_invite_link(int(chat_id), mode)
        except Exception as e:
            print(f"Error cleaning up invalid link {key}: {e}")
    
    if invalid_keys:
        print(f"🧹 Cleaned up {len(invalid_keys)} invalid invite links")


#=====================================================================================##

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client, message: Message):
    total = await db.get_total_verify_count()
    await message.reply_text(f"Tᴏᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴋᴇɴs ᴛᴏᴅᴀʏ: <b>{total}</b>")


#=====================================================================================##

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)