from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""⎆ اهلا بـك عزيـزي 

⎆ يمكنك استـخـراج التالـي

⎆ تيرمڪس تليثون للحسابات

⎆ تيرمـكـس تليثون للبوتـات

⎆ بايـروجـرام مـيوزك للحسابات

⎆ بايـروجـرام مـيوزك للبوتات

⎆ تم انشاء البوت بواسطة  [ㅤ𓏺 𝗘𝗟𝗚𝗔𝗭𝗔𝗥. 🕷 ˼](https://t.me/A_M_0_3)""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⎆بـدء استخـراج الجلسـة", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("⎆قنـاة السـورس", url="https://t.me/A_M_030"),
                    InlineKeyboardButton("⎆المطـور", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
