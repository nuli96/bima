import aiohttp
import filetype
from io import BytesIO
from PyroUbot import *
from httpx import AsyncClient, Timeout

fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)

async def upload_file(buffer: BytesIO) -> str:
    kind = filetype.guess(buffer)
    if kind is None:
        raise ValueError("Cannot determine file type")
    ext = kind.extension

    buffer.seek(0)
    form = aiohttp.FormData()
    form.add_field(
        'fileToUpload',
        buffer,
        filename='file.' + ext,
        content_type=kind.mime
    )
    form.add_field('reqtype', 'fileupload')

    async with aiohttp.ClientSession() as session:
        async with session.post('https://catbox.moe/user/api.php', data=form) as response:
            if response.status != 200:
                raise Exception(f"Failed to upload file: {response.status}")
            return await response.text()

__MODULE__ = "ᴛᴏᴜʀʟ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Tourl

perintah : <code>{0}tourl</code> [ replay media ]
    mengupload media ke link</blockquote></b>

"""

@PY.UBOT("tourl|tg")
async def _(client, message):
    reply_message = message.reply_to_message
    if reply_message and reply_message.media:
        downloaded_file = await reply_message.download()
        
        with open(downloaded_file, 'rb') as f:
            buffer = BytesIO(f.read())
            try:
                media_url = await upload_file(buffer)
                await message.reply(f"<b>Succes Upload Ke : <a href='{media_url}'>link fotomu</a></b>")
            except Exception as e:
                await message.reply(f"Error: {e}")
    else:
        await message.reply("Please reply to a media message to upload.")
