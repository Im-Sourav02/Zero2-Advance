
import asyncio
import os
import random
import sys
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, InviteHashEmpty, ChatAdminRequired, PeerIdInvalid, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

#Request force sub mode commad,,,,,,
@Bot.on_message(filters.command('fsub_mode') & filters.private & admin)
async def change_force_sub_mode(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        return await temp.edit("<b>❌ No force-sub channels found.</b>")

    buttons = []
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            mode = await db.get_channel_mode(ch_id)
            status = "🟢" if mode == "on" else "🔴"
            title = f"{status} {chat.title}"
            buttons.append([InlineKeyboardButton(title, callback_data=f"rfs_ch_{ch_id}")])
        except:
            buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"rfs_ch_{ch_id}")])

    buttons.append([InlineKeyboardButton("Close ✖️", callback_data="close")])

    await temp.edit(
        "<b>⚡ Select a channel to toggle Force-Sub Mode:</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# This handler captures membership updates (like when a user leaves, banned)
@Bot.on_chat_member_updated()
async def handle_Chatmembers(client, chat_member_updated: ChatMemberUpdated):    
    chat_id = chat_member_updated.chat.id

    if await db.reqChannel_exist(chat_id):
        old_member = chat_member_updated.old_chat_member

        if not old_member:
            return

        if old_member.status == ChatMemberStatus.MEMBER:
            user_id = old_member.user.id

            if await db.req_user_exist(chat_id, user_id):
                await db.del_req_user(chat_id, user_id)


# This handler will capture any join request to the channel/group where the bot is an admin
@Bot.on_chat_join_request()
async def handle_join_request(client, chat_join_request):
    chat_id = chat_join_request.chat.id
    user_id = chat_join_request.from_user.id

    #print(f"[JOIN REQUEST] User {user_id} sent join request to {chat_id}")

    # Print the result of db.reqChannel_exist to check if the channel exists
    channel_exists = await db.reqChannel_exist(chat_id)
    #print(f"Channel {chat_id} exists in the database: {channel_exists}")

    if channel_exists:
        if not await db.req_user_exist(chat_id, user_id):
            await db.req_user(chat_id, user_id)
            #print(f"Added user {user_id} to request list for {chat_id}")


# Add channel
@Bot.on_message(filters.command('addchnl') & filters.private & admin)
async def add_force_sub(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    args = message.text.split(maxsplit=1)

    if len(args) != 2:
        return await temp.edit(
            "<b>Usage:</b> <code>/addchnl -100XXXXXXXXXX</code>\n<b>Add only one channel at a time.</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ✖️", callback_data="close")]])
        )

    try:
        channel_id = int(args[1])
    except ValueError:
        return await temp.edit("<b>❌ Invalid Channel ID!</b>")

    all_channels = await db.show_channels()
    channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
    if channel_id in channel_ids_only:
        return await temp.edit(f"<b>Channel already exists:</b> <code>{channel_id}</code>")

    try:
        chat = await client.get_chat(channel_id)

        if chat.type != ChatType.CHANNEL:
            return await temp.edit("<b>❌ Only public or private channels are allowed.</b>")

        member = await client.get_chat_member(chat.id, "me")
        print(f"Bot status: {member.status} in chat: {chat.title} ({chat.id})")  # Debug

        # FIXED ENUM COMPARISON
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await temp.edit("<b>❌ Bot must be an admin in that channel.</b>")

        # Get invite link
        try:
            link = await client.export_chat_invite_link(chat.id)
        except Exception:
            link = f"https://t.me/{chat.username}" if chat.username else f"https://t.me/c/{str(chat.id)[4:]}"

        await db.add_channel(channel_id)
        return await temp.edit(
            f"<b>✅ Force-sub channel added successfully!</b>\n\n"
            f"<b>Name:</b> <a href='{link}'>{chat.title}</a>\n"
            f"<b>ID:</b> <code>{channel_id}</code>",
            disable_web_page_preview=True
        )

    except Exception as e:
        return await temp.edit(
            f"<b>❌ Failed to add channel:</b>\n<code>{channel_id}</code>\n\n<i>{e}</i>"
        )


# Delete channel
@Bot.on_message(filters.command('delchnl') & filters.private & admin)
async def del_force_sub(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    args = message.text.split(maxsplit=1)
    
    try:
        # Get all channels
        all_channels = await db.show_channels()
        
        # Debug information 
        channel_info = f"Found {len(all_channels) if all_channels else 0} channels in database."
        print(channel_info)
        
        if not all_channels:
            return await temp.edit("<b>❌ No force-sub channels found.</b>")
            
        # Format all channels for display
        channel_list = []
        for ch_item in all_channels:
            if isinstance(ch_item, tuple) and len(ch_item) >= 1:
                ch_id = ch_item[0]
            elif isinstance(ch_item, (int, str)):
                ch_id = int(ch_item)
            elif hasattr(ch_item, 'get'):
                ch_id = ch_item.get('chat_id') or ch_item.get('id')
            else:
                ch_id = str(ch_item)  # Just stringify it as fallback
            channel_list.append(str(ch_id))
            
        # Check command format
        if len(args) != 2:
            all_channels_str = "\n".join([f"• <code>{ch}</code>" for ch in channel_list])
            return await temp.edit(
                f"<b>Usage:</b> <code>/delchnl &lt;channel_id | all&gt;</code>\n\n"
                f"<b>Available channels:</b>\n{all_channels_str}"
            )

        # Handle "all" command
        if args[1].lower() == "all":
            success_count = 0
            for ch_item in all_channels:
                try:
                    if isinstance(ch_item, tuple) and len(ch_item) >= 1:
                        ch_id = ch_item[0]
                    elif isinstance(ch_item, (int, str)):
                        ch_id = int(ch_item)
                    elif hasattr(ch_item, 'get'):
                        ch_id = ch_item.get('chat_id') or ch_item.get('id')
                    else:
                        ch_id = ch_item
                        
                    # Try both functions for compatibility
                    try:
                        await db.rem_channel(ch_id)
                        success_count += 1
                    except Exception:
                        await db.del_channel(ch_id)
                        success_count += 1
                except Exception as e:
                    print(f"Error removing channel {ch_item}: {e}")
                    
            return await temp.edit(f"<b>✅ {success_count}/{len(all_channels)} force-sub channels have been removed.</b>")

        # Handle specific channel ID
        try:
            ch_id = int(args[1])
        except ValueError:
            return await temp.edit("<b>❌ Invalid Channel ID. Please provide a valid numeric ID.</b>")

        # Check if channel ID exists in any format
        channel_found = False
        for ch_item in all_channels:
            item_id = None
            if isinstance(ch_item, tuple) and len(ch_item) >= 1:
                item_id = ch_item[0]
            elif isinstance(ch_item, (int, str)):
                item_id = int(ch_item)
            elif hasattr(ch_item, 'get'):
                item_id = ch_item.get('chat_id') or ch_item.get('id')
            else:
                try:
                    item_id = int(ch_item)
                except:
                    item_id = ch_item
                    
            if item_id == ch_id:
                channel_found = True
                break
                
        if channel_found:
            # Try both functions for compatibility
            try:
                success = await db.rem_channel(ch_id)
            except Exception as e1:
                try:
                    success = await db.del_channel(ch_id)
                except Exception as e2:
                    return await temp.edit(
                        f"<b>❌ Error removing channel:</b> <code>{ch_id}</code>\n"
                        f"<b>Errors:</b>\n"
                        f"• rem_channel: {e1}\n"
                        f"• del_channel: {e2}"
                    )
                    
            return await temp.edit(f"<b>✅ Channel removed:</b> <code>{ch_id}</code>")
        else:
            all_channels_str = "\n".join([f"• <code>{ch}</code>" for ch in channel_list])
            return await temp.edit(
                f"<b>❌ Channel not found in force-sub list:</b> <code>{ch_id}</code>\n\n"
                f"<b>Available channels:</b>\n{all_channels_str}"
            )
            
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return await temp.edit(
            f"<b>❌ An error occurred:</b>\n<code>{e}</code>\n\n"
            f"<details>\n<summary>Error details</summary>\n<pre>{tb}</pre>\n</details>"
        )

# View all channels
@Bot.on_message(filters.command('listchnl') & filters.private & admin)
async def list_force_sub_channels(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        return await temp.edit("<b>❌ No force-sub channels found.</b>")

    result = "<b>⚡ Force-sub Channels:</b>\n\n"
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            link = chat.invite_link or await client.export_chat_invite_link(chat.id)
            result += f"<b>•</b> <a href='{link}'>{chat.title}</a> [<code>{ch_id}</code>]\n"
        except Exception:
            result += f"<b>•</b> <code>{ch_id}</code> — <i>Unavailable</i>\n"

    await temp.edit(result, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ✖️", callback_data="close")]]))
    