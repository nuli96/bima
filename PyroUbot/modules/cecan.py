from PyroUbot import *
import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO

__MODULE__ = "ᴄᴇᴄᴀɴ"
__HELP__ = """
<blockquote><b>『 ʙᴀɴᴛᴜᴀɴ ᴄᴇᴄᴀɴ 』</b>

<b>⌲ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}cecan [query]</code>

<b>Query:</b> <b>Indonesia</b>,
    <b>china</b>,
    <b>thailand</b>,
    <b>vietnam</b>,
    <b>hijaber</b>,
    <b>rose</b>,
    <b>ryujin</b>,
    <b>jiso</b>,
    <b>jeni</b>,
    <b>justinaxie</b>,
    <b>malaysia</b>,
    <b>japan</b>,
    <b>korea</b></blockquote>
"""

URLS = {
    "indonesia": "https://api.botcahx.eu.org/api/cecan/indonesia?apikey=kepo",
    "china": "https://api.botcahx.eu.org/api/cecan/china?apikey=kepo",
    "thailand": "https://api.botcahx.eu.org/api/cecan/thailand?apikey=kepo",
    "vietnam": "https://api.botcahx.eu.org/api/cecan/vietnam?apikey=kepo",
    "hijaber": "https://api.botcahx.eu.org/api/cecan/hijaber?apikey=kepo",
    "rose": "https://api.botcahx.eu.org/api/cecan/rose?apikey=kepo",
    "ryujin": "https://api.botcahx.eu.org/api/cecan/ryujin?apikey=kepo",
    "jiso": "https://api.botcahx.eu.org/api/cecan/jiso?apikey=kepo",
    "jeni": "https://api.botcahx.eu.org/api/cecan/jeni?apikey=kepo",
    "justinaxie": "https://api.botcahx.eu.org/api/cecan/justinaxie?apikey=kepo",
    "malaysia": "https://api.botcahx.eu.org/api/cecan/malaysia?apikey=kepo",
    "japan": "https://api.botcahx.eu.org/api/cecan/japan?apikey=kepo",
    "korea": "https://api.botcahx.eu.org/api/cecan/korea?apikey=kepo"
}

@PY.UBOT("cecan")
@PY.TOP_CMD
async def _(client, message):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("Processing...")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar cecan Error: {e}")
