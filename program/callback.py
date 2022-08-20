# Copyright (C) 2021 By logiMusicProject

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Welcome [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Yeni Telegram'ın görüntülü sohbetleri aracılığıyla gruplarda müzik ve video oynatmanıza izin verir!**

💡 **Bot'un tüm komutlarını ve nasıl çalıştıklarını öğrenmek için » 📚 Commands button!**


🛠 [🕊](https://t.me/ruhsuzbeyyy) **Herhangi bir sorununuz varsa iletişim**

❔ **Bu botun nasıl kullanılacağını öğrenmek için lütfen » ❓ Temel Kılavuz düğmesi!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ beni grubuna ekle ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Temel Kılavuz", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 Komut", callback_data="cbcmds"),
                    InlineKeyboardButton("❤ sahip", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "🕊️", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "💜", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🖤", url="https://t.me/ruhsuzbeyyy"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **Bu botu kullanmak için Temel Kılavuz:**

1.) **önce beni grubunuza ekleyin.**
 2.) **sonra beni yönetici olarak tanıtın ve anonim yönetici hariç tüm izinleri verin.**
 3.) **Grubunuza @{ASSISTANT_NAME} ekleyin veya onu davet etmek için /userbotjoin yazın.**
 4.) **videoyu oynatmaya başlamadan önce görüntülü sohbeti açın.**
 5.) ** » 📚 Komutlar düğmesinde görebileceğiniz tüm komut listesi, başlangıç ​​ana sayfasında bulun, aşağıdaki » Geri Dön düğmesine dokunun.**
💡 **Bu bot hakkında takip eden sorularınız varsa, destek sohbetimde buradan anlayabilirsiniz: @{GROUP_SUPPORT}**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 geri", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""📚 İşte Komutlar listesi:

» /play - sesli sohbette müzik çal
 » /stream - radyo bağlantısını girin
 » /vplay - görüntülü sohbette video oynatın
 » /vstream - m3u8/canlı bağlantı için
 » /playlist - size çalma listesini gösterir
 » /video (sorgu) - youtube'dan video indir
 » /song (sorgu) - youtube'dan şarkı indir
 » /lyric (sorgu) - şarkı sözlerini not edin
 » /search (sorgu) - bir youtube video bağlantısında arama yapın
 » /queue - sıra listesini gösterir (yalnızca yönetici)
 » /pause - akışı duraklatın (yalnızca yönetici)
 » /resume - akışı devam ettir (yalnızca yönetici)
 » /skip - sonraki akışa geç (yalnızca yönetici)
 » /stop - akışı durdur (yalnızca yönetici)
 » /userbotjoin - userbot'u sohbete katılmaya davet edin (yalnızca yönetici)
 » /userbotleave - userbot'un gruptan ayrılmasını emreder (yalnızca yönetici)
 » /reload - yönetici listesini güncelle (yalnızca yönetici)
 » /rmw - ham dosyaları temizle (yalnızca sudo)
 » /rmd - indirilen dosyaları temizle (yalnızca sudo)
 » /leaveall - userbot'un tüm gruptan ayrılmasını emreder (yalnızca sudo)
⚡ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙geri", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    await query.message.delete()
