#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiAFKBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiAFKBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

from typing import Union
from datetime import datetime, timedelta
from Yukki import cleanmode, app, botname
from Yukki.database import is_cleanmode_on
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


async def put_cleanmode(chat_id, message_id):
    if chat_id not in cleanmode:
        cleanmode[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=5),
    }
    cleanmode[chat_id].append(put)


async def auto_clean():
    while not await asyncio.sleep(30):
        try:
            for chat_id in cleanmode:
                if not await is_cleanmode_on(chat_id):
                    continue
                for x in cleanmode[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        except:
                            continue
                    else:
                        continue
        except:
            continue


asyncio.create_task(auto_clean())


RANDOM = [
    "https://te.legra.ph/file/95156831eb10e700ed255.jpg",
    "https://te.legra.ph/file/fb8d6318051d8ab540876.jpg",
    "https://te.legra.ph/file/5adad29bb8aabc7a4d581.jpg",
    "https://te.legra.ph/file/d2c3125f0329afb9703f1.jpg",
    "https://te.legra.ph/file/b08622f7d74ff089c90ad.jpg",
    "https://te.legra.ph/file/80fd0e0e64854867ba389.jpg",
    "https://te.legra.ph/file/ab6e053adfdd62311a9b1.jpg",
    "https://te.legra.ph/file/47ea646ae7fcfc1e63997.jpg",
    "https://te.legra.ph/file/4b430f271aefeae9dfa58.jpg",
    "https://te.legra.ph/file/6cf4f5fb8402f937b1700.jpg",
    "https://te.legra.ph/file/5ae9c12d94893c5fc7952.jpg",
    "https://te.legra.ph/file/5ae9c12d94893c5fc7952.jpg",
]


HELP_TEXT = f"""Welcome to {botname} Help Section.

▷ **When someone mentions you in a chat, the user will be notified you are AFK. You can even provide a reason for going AFK, which will be provided to the user as well.**


/afk - This will set you offline.

/afk [Reason] - This will set you offline with a reason.

/afk [Replied to a Sticker/Photo] - This will set you offline with an image or sticker.

/afk [Replied to a Sticker/Photo] [Reason] - This will set you afk with an image and reason both.


▷ **Bot Owner: @The_Sneha_Singh** 🫶🏻
"""

def settings_markup(status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="🔄 Clean Mode", callback_data="cleanmode_answer"),
            InlineKeyboardButton(
                text="✅ Enabled" if status == True else "❌ Disabled",
                callback_data="CLEANMODE",
            ),
        ],
        [
            InlineKeyboardButton(text="🗑 Close Menu", callback_data="close"),
        ],
    ]
    return buttons
