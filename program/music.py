# Copyright (C) 2021 By logi music-player
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, OWNER_NAME
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.logi import call_py, user
from driver.utils import bash
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'youtube-dl -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@Client.on_message(command(["play", f"mplay@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="⏭️atla", callback_data="cskip"),
                InlineKeyboardButton(text="⏹️dur", callback_data="cpause"),
                InlineKeyboardButton(text="•❌kapaᴇ", callback_data="cls"), 
            ],
             [
                    InlineKeyboardButton(
                        "🕊", url=f"https://t.me/{OWNER_NAME}"
                    )
                ],
        ]
    )
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için aşağıdaki **izinlere sahip bir **Yönetici** olmam gerekiyor**:\n\n» ❌ __İletileri silme__\n» ❌ __kullanıcı ekleme__\n» ❌ _Manage video chat_\n\nVeriler **Güncel -leştirilmiş** sizden sonra otomatik olarak **beni yönteci yap**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "gerekli izin eksik:" + "\n\n» ❌ __Manage video chat__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "gerekli izin eksik:" + "\n\n» ❌ __Delete messages__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\n» ❌ __Add users__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **grupta yasaklandı** {m.chat.title}\n\n» **Bu botu kullanmak istiyorsanız önce kullanıcı botunun yasağını kaldırın.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot katılamadı**\n\n**sebep**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot katılamadı**\n\n**sebep**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **ses indiriliyor...**⚡")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **parça kuyruğa eklendi »** `{pos}`\n\n🏷 **isim:** [{songname}]({link}) | `music`\n💭 **grub:** `{chat_id}`\n🎧 **ekleyen🕊️by:** {m.from_user.mention()} \n💚**Herhangi bir sorun iletişim :** [🍂👣🌿](https://t.me/ruhsuzbeyyy)",
                    reply_markup=keyboard,
                )
            else:
             try:
                await suhu.edit("♻️ **sese katılıyor...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"📡🎶**Adı** [{songname}]({link})\n💭 **Chatıd:** `{chat_id}`\n💡 **Durum:** 'Oynatıyor '\n🎧 **İstek gönderen:** {requester}\n📹 **Akış türü:** `Music` \n💚 iyi dinlemeler🍂💜🌿",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» merhaba sesli veya vidyo oynatmak için türünü seçin.**"
                )
            else:
                suhu = await c.send_message(chat_id, "👣")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **sonuç bulunamadı.**")
                else:
                    songname = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    format = "bestaudio[ext=m4a]"
                    logi, ytlink = await ytdl(format, url)
                    if logi == 0:
                        await suhu.edit(f"❌ yt-dl sorunları algılandı\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"🍂👣🌿 **Takip kuyruğa eklendi »** `{pos}`\n\n🌒 **Adı:** [{songname}]({url}) | `muzik`\n**⏱ Süre:** `{duration}`\n🎧 **isteyen by:** {requester} \n🍂**Herhangi bir sorun iletişim 📡:** [🕊️TeknikDestek](https://t.me/ruhsuzbeyyy)",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("📡**sese katılıyor 🌖..**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=thumbnail,
                                    caption=f"🎼**Adı:** [{songname}]({url})\n**⏱ Süre:** `{duration}`\n💡 **Durum:** `Oynatıyor `\n🎧 **isteyen by:** {requester}\n📹 **Akış türü:** `Muzik` \n💚**Herhangi bir sorun iletişim :** [🍂👣🌿](https://t.me/ruhsuzbeyyy)",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» bir **ses dosyası** yada **aramak için bir şey ver.**"
            )
        else:
            suhu = await c.send_message(chat_id, "👣")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **no results found.**")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                format = "bestaudio[ext=m4a]"
                logi, ytlink = await ytdl(format, url)
                if logi == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=thumbnail,
                            caption=f"🍂👣🌿 **Takip kuyruğa eklendi »** `{pos}`\n\n🌘**Adı:** [{songname}]({url}) | `music`\n**⏱ Süre:** `{duration}`\n🎧 **Request by:** {requester}\n💚**sponsor :** [🕊KorSan💜🌿](https://t.me/CanliSohbetGruplari)",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("♻️ **katılıyor.**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"🎶📡⚡ **Adı:** [{songname}]({url})\n**⏱ süre:** `{duration}`\n🌘**Durum:** `Oynatılıyor`\n🎧 **isteyen🕊️ by:** {requester}\n📹 **Çalma türü:** `Muzik`\n💚**sponsor🕊️:** [💜Korsan🌿](https://t.me/CanliSohbetGruplari)",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")
