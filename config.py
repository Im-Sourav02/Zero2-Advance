import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

#--------------------------------------------
#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "@Im_Sukuna02")
APP_ID = int(os.environ.get("APP_ID", "@Im_Sukuna02")) #Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "@Im_Sukuna02") #Your API Hash from my.telegram.org
#--------------------------------------------

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "@Im_Sukuna02")) #Your db channel Id 
OWNER = os.environ.get("OWNER", "Im_Sukuna02") # Owner username without @
OWNER_ID = int(os.environ.get("OWNER_ID", "@Im_Sukuna02")) # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8001")
#--------------------------------------------
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Im_Sukuna02")
#--------------------------------------------
FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "10"))  # 0 means no expiry
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "@Im_Sukuna02")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
#--------------------------------------------
START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/7d5ng3jr/photo-2025-05-17-09-26-38-7505343723559976972.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.ibb.co/7d5ng3jr/photo-2025-05-17-09-26-38-7505343723559976972.jpg")
#--------------------------------------------
SHORTLINK_API = os.environ.get("SHORTLINK_API", "@Im_Sukuna02")  # Default Shortlink API
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "linkshortify.com")  # Default Shortlink URL
SHORT_MSG = "<b>⌯ Here is Your Download Link, Must Watch Tutorial Before Clicking On Download...</b>"

SHORTENER_PIC = os.environ.get("SHORTENER_PIC", "https://i.ibb.co/7d5ng3jr/photo-2025-05-17-09-26-38-7505343723559976972.jpg")

#--------------------------------------------
TUT_VID = "https://t.me/Infinity_0034/9"
#--------------------------------------------
HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ ᴡᴏʀᴋ ғᴏʀ @InFinity_Adult\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!</blockquote></b>"
ABOUT_TXT = "<b><blockquote>◈ ᴏᴡɴᴇʀ : <a href=t.me/Im_Sukuna02>ɪᴍ•Ꮪᴜ͢ᴋᴜɴᴀ</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/Infinix_Syndicate>ɪɴғɪɴɪx sʏɴᴅɪᴄᴀᴛᴇ</a>\n◈ ᴍᴏᴠɪᴇs ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Infinix_Movie>ɪɴғɪɴɪx ᴍᴏᴠɪᴇs</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/ProYato>ʏᴀᴛᴏ</a></blockquote></b>"

#--------------------------------------------
START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote> ɪ ᴀᴍ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.</blockquote></b>")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</blockquote></b>")

CMD_TXT = """<blockquote><b>» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b></blockquote>

<b>›› /dlt_time :</b> sᴇᴛ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ
<b>›› /check_dlt_time :</b> ᴄʜᴇᴄᴋ ᴄᴜʀʀᴇɴᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ
<b>›› /dbroadcast :</b> ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏᴄᴜᴍᴇɴᴛ / ᴠɪᴅᴇᴏ
<b>›› /ban :</b> ʙᴀɴ ᴀ ᴜꜱᴇʀ
<b>›› /unban :</b> ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ
<b>›› /banlist :</b> ɢᴇᴛ ʟɪsᴛ ᴏꜰ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀs
<b>›› /addchnl :</b> ᴀᴅᴅ ꜰᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /delchnl :</b> ʀᴇᴍᴏᴠᴇ ꜰᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /listchnl :</b> ᴠɪᴇᴡ ᴀᴅᴅᴇᴅ ᴄʜᴀɴɴᴇʟs
<b>›› /fsub_mode :</b> ᴛᴏɢɢʟᴇ ꜰᴏʀᴄᴇ sᴜʙ ᴍᴏᴅᴇ
<b>›› /pbroadcast :</b> sᴇɴᴅ ᴘʜᴏᴛᴏ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀs
<b>›› /add_admin :</b> ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ
<b>›› /deladmin :</b> ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ
<b>›› /admins :</b> ɢᴇᴛ ʟɪsᴛ ᴏꜰ ᴀᴅᴍɪɴs
<b>›› /addpremium :</b> ᴀᴅᴅ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ
<b>›› /premium_users :</b> ʟɪsᴛ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀs
<b>›› /remove_premium :</b> ʀᴇᴍᴏᴠᴇ ᴘʀᴇᴍɪᴜᴍ ꜰʀᴏᴍ ᴀ ᴜꜱᴇʀ
<b>›› /myplan :</b> ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs
<b>›› /count :</b> ᴄᴏᴜɴᴛ verifications
<b>›› /ping :</b> ᴄʜᴇᴄᴋ ʙᴏᴛ ʟᴀᴛᴇɴᴄʏ
<b>›› /uptime :</b> ᴄʜᴇᴄᴋ ʙᴏᴛ ʀᴜɴᴛɪᴍᴇ
<b>›› /logs :</b> ɢᴇᴛ ʀᴇᴄᴇɴᴛ ʙᴏᴛ ʟᴏɢs
<b>›› /restart :</b> ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
<b>›› /addforcepic :</b> ᴀᴅᴅ ғᴏʀᴄᴇ sᴜʙ ᴘɪᴄᴛᴜʀᴇ
<b>›› /addstartpic :</b> ᴀᴅᴅ sᴛᴀʀᴛ sᴜʙ ᴘɪᴄᴛᴜʀᴇ
<b>›› /delforcepic :</b> ᴅᴇʟᴇᴛᴇ ғᴏʀᴄᴇ sᴜʙ ᴘɪᴄᴛᴜʀᴇ
<b>›› /delstartpic :</b> ᴅᴇʟᴇᴛᴇ sᴛᴀʀᴛ sᴜʙ ᴘɪᴄᴛᴜʀᴇ
<b>›› /showforcepic :</b> sʜᴏᴡ ᴀʟʟ ғᴏʀᴄᴇ sᴜʙ ᴘɪᴄᴛᴜʀᴇs
<b>›› /showstartpic :</b> sʜᴏᴡ ᴀʟʟ sᴛᴀʀᴛ sᴜʙ ᴘɪᴄᴛᴜʀᴇs
<b>›› /shortner :</b> ᴇᴅɪᴛ sʜᴏʀᴛʟɪɴᴋ ᴜʀʟ ᴀɴᴅ ᴀᴘɪ
<b>›› /edittutvid :</b> ᴇᴅɪᴛ ᴛᴜᴛᴏʀɪᴀʟ ᴠɪᴅᴇᴏ ᴜʀʟ
<b>›› /showshortner :</b> sʜᴏᴡ ᴄᴜʀʀᴇɴᴛ sʜᴏʀᴛʟɪɴᴋ sᴇᴛᴛɪɴɢs
"""
#--------------------------------------------
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ @infinix_adult</b>") #set your Custom Caption here, Keep None for Disable Custom Caption
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False #set True if you want to prevent users from forwarding files from bot
#--------------------------------------------
#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'
#--------------------------------------------
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"
#--------------------------------------------

#==========================(BUY PREMIUM)====================#

OWNER_TAG = os.environ.get("OWNER_TAG", "Im_Sukuna02")
UPI_ID = os.environ.get("UPI_ID", "imsukuna@upi")
QR_PIC = os.environ.get("QR_PIC", "https://i.ibb.co/7Jb0Y61Z/photo-2025-05-08-12-47-46-7502782230834446396.jpg")
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"t.me/Im_Sukuna02")
#--------------------------------------------
#Time and its price
#7 Days
PRICE1 = os.environ.get("PRICE1", "0 rs")
#1 Month
PRICE2 = os.environ.get("PRICE2", "60 rs")
#3 Month
PRICE3 = os.environ.get("PRICE3", "150 rs")
#6 Month
PRICE4 = os.environ.get("PRICE4", "280 rs")
#1 Year
PRICE5 = os.environ.get("PRICE5", "550 rs")

#===================(END)========================#

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
