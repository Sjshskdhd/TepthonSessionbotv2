from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "⎆**• ذا كنت تريد تنصب ميوزك اختار بايروجرام\n\n• واذا تريد تنصب تليثون فأختار تيرمڪس\n\n• يوجد استخرجات جلسات لي البوتات**"


buttons_ques = [
    [
        InlineKeyboardButton("⎆بـايـروجـرام", callback_data="pyrogram"),
        InlineKeyboardButton("⎆تيـرمكـس", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("⎆بايروجـرام بوت", callback_data="pyrogram_bot"),
        InlineKeyboardButton("⎆تليثـون بوت", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="⎆بـدء استخـراج الجلسـة", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "تيرمكـس"
    else:
        ty = "بايروجـرام"
    if is_bot:
        ty += " بوت"
    await msg.reply(f"⎆ ⚡ ¦ بـدء إنـشـاء جـلسـة **{ty}** ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "🎮حسنـا قم بأرسال الـ API_ID\n\nاضغط /skip عشان تكمل بالموجدين", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("⎆ **الأيبـي أيـدي الخـاص بـك غيـر صـالح يرجـى إعـادة استخـراج الجلسـة مـرة أخـرى.**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "**⎆🎮حسنـا قم بأرسال الـ API_HASH**", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "**⎆ يـرجـى إرسـال رقـم هاتفـك مـع رمـز الدولة مثــال 📱: +201098906252**"
    else:
        t = "⎆ ** يرجـى إرسـال توكـن بوتـك مثــال ⭐ : 5396274279:hshhshshshshss`'**'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("**⎆جـاري إرسـال الكـود إلـى حسـابك ...**")
    else:
        await msg.reply("يحـاول التسجيـل عبر التوكـن ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("**⎆ الأيبـي أيـدي والأيبـي هـاش غير صالحـان أعـد استخـراج الجلسـة مـرة أخـرى .**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("**⎆ رقـم الهـاتف الذي أرسلـته غير صالح أعـد استخـراج الجلسـة مـرة أخـرى .**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "⎆[ارسل الكود زي اللي في الصوره](https://telegra.ph/file/da1af082c6b754959ab47.jpg)» 🔍من فضلك افحص حسابك بالتليجرام وتفقد الكود من حساب اشعارات التليجرام. إذا كان\n  هناك تحقق بخطوتين( المرور ) ، أرسل كلمة المرور هنا بعد ارسال كود الدخول بالتنسيق أدناه.- اذا كانت كلمة المرور او الكود  هي\n 12345 يرجى ارسالها بالشكل التالي 1 2 3 4 5 مع وجود مسـافـات بين الارقام اذا احتجت مساعدة @A_M_0_3.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply(" **⎆ انـتـهـت المـدة يرجى إعادة الاستخراج مرة أخرى**", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("**⎆ الكـود الخـاص بـك غير صالـحn/أعد استخـراج الجلسـة مـرة أخـرى**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("**⎆ انتهت مـدة الكـودn/أعـد استخـراج الجلسـة مـرة أخـرى**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "** ⎆ يـرجـى إرسـال التحقق الخـاص بحسـابك ..**", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("**⎆ انـتـهـت المـدة يرجى إعادة الاستخراج مرة أخرى**", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("⎆التحقـق بخطوتيـن الخـاص بـك غيـر صـالح.\n\nيرجـى إعـادة استخـراج الجلسـة مـرة أخـرى", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**⎆كـود {ty} ☑️**\n\n`{string_session}` \n\n**⎆تم الاستخـراج بواسطـة @A_M_30_bot**"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "⎆تم استخـراج كـود جلسـة {} .. بنجـاح ✅\n\n ⎆تم ارسـال الكـود لحافظـة حسـابـك للامـان 😇".format("تـيـرمـكس" if telethon else "بـايـروجـرام"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**⎆تم إلغـاء استخـراج الجلسـة !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» تمـ آعآدهہ‏‏ آلتشـغيـل مـن تآنيـﮯ يـبرو !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**⎆تـم الـتـخـطـي**", quote=True)
        return True
    else:
        return False
