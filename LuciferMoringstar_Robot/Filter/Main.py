# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from OMDB import get_movie_info
import re
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
import random
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📢 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📢", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🗂️ 𝗧𝗶𝘁𝗹𝗲:** {search}\n**⭐ 𝗥𝗮𝘁𝗶𝗻𝗴:** {random.choice(RATING)}\n**🎭 𝗚𝗲𝗻𝗿𝗲:** {random.choice(GENRES)}\n**🗳️ 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗱 𝗕𝘆: {message.chat.title}**"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADMwIAAtbcmFelnLaGAZhgBwI')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text=" 🌹 𝗣𝗮𝗴𝗲𝘀 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝗡𝗲𝘅𝘁 ➡️",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f" 🌹 𝗣𝗮𝗴𝗲𝘀 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    movie_name = message.text
    movie_info = get_movie_info(movie_name)
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        mo_tech_yt = f"""<b>📽 𝗠𝗼𝘃𝗶𝗲 𝗡𝗮𝗺𝗲  : {movie_info['title']}</b>

<b>⏱️ 𝗥𝘂𝗻𝘁𝗶𝗺𝗲 : {movie_info['duration']}</b>
<b>🌟 𝗜𝗠𝗗𝗯 𝗥𝗮𝘁𝗶𝗻𝗴 : {movie_info['imdb_rating']}/10</b>

📧 𝗩𝗼𝘁𝗲𝘀 : <b>{movie_info['votes']}</b>
📆 𝗥𝗲𝗹𝗲𝗮𝘀𝗲 : <b>{movie_info['release']}</b>
🎞️ 𝗚𝗲𝗻𝗿𝗲 : <b>{movie_info['genre']}</b>
🔊 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲𝘀 : <b>{movie_info['language']}</b>
👩🏻‍💻 𝗖𝗮𝘀𝘁 : <b>{movie_info['actors']}</b>
🏞️ 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 : <b>{movie_info['country']}</b>
🎬 𝗗𝗶𝗿𝗲𝗰𝘁𝗼𝗿 : <b>{movie_info['director']}</b>
📝 𝗪𝗿𝗶𝘁𝗲𝗿 : <b>{movie_info['writer']}</b>


📜 **Plot** : <code><b>{movie_info['plot']}</b></code>"""
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=pr0fess0r_99_-_-_-_{file_id}")]
               )
        else:
            LuciferMoringstar=await client.send_video(
        chat_id=message.chat.id,
        video="https://telegra.ph/file/c2c0ff4b927dcc50e7922.mp4",
        caption=f"""𝗛𝗲𝘆..❤‍🔥 <b>{message.from_user.mention}</b>
𝗜𝗳 𝘁𝗵𝗶𝘀 𝗺𝗼𝘃𝗶𝗲 𝗶𝘀 𝗻𝗼𝘁 𝗶𝗻 𝗼𝘂𝗿 𝗱𝗮𝘁𝗮𝗯𝗮𝘀𝗲 𝘆𝗼𝘂 𝘄𝗶𝗹𝗹 𝗻𝗼𝘁 𝗴𝗲𝘁 𝘁𝗵𝗮𝘁 𝗺𝗼𝘃𝗶𝗲..
𝗢𝘁𝗵𝗲𝗿𝘄𝗶𝘀𝗲, 𝘁𝗵𝗲 𝘀𝗽𝗲𝗹𝗹𝗶𝗻𝗴 𝗼𝗳 𝘁𝗵𝗲 𝗻𝗮𝗺𝗲 𝗼𝗳 𝘁𝗵𝗲 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗺𝗼𝘃𝗶𝗲 𝗺𝗮𝘆 𝗻𝗼𝘁 𝗯𝗲 𝗰𝗼𝗿𝗿𝗲𝗰𝘁...
𝗦𝗼 𝘆𝗼𝘂 𝗴𝗼 𝘁𝗼 𝗚𝗼𝗼𝗴𝗹𝗲 𝗮𝗻𝗱 𝗰𝗵𝗲𝗰𝗸 𝘁𝗵𝗲 𝘀𝗽𝗲𝗹𝗹𝗶𝗻𝗴 𝗼𝗳 𝘁𝗵𝗲 𝗻𝗮𝗺𝗲 𝗼𝗳 𝘁𝗵𝗲 𝗺𝗼𝘃𝗶𝗲 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁.𝗢𝗿 𝗔𝘀𝗸 𝗠𝗲 ›› @BKC0001

<b>ഈ സിനിമ ഞങ്ങളുടെ ഡാറ്റാബേസിൽ ഇല്ലെങ്കിൽ നിങ്ങൾക്ക് ഈ സിനിമ ലഭിക്കില്ല
അല്ലെങ്കിൽ, അഭ്യർത്ഥിച്ച സിനിമയുടെ പേരിന്റെ അക്ഷരവിന്യാസം ശരിയായിരിക്കില്ല ...
അതിനാൽ നിങ്ങൾ ഗൂഗിളിൽ പോയി നിങ്ങൾക്ക് ആവശ്യമുള്ള സിനിമയുടെ പേരിന്റെ സ്പെല്ലിംഗ് പരിശോധിക്കുക.. അല്ലെങ്കിൽ എന്നോട് പറയുക ›› @BKC0001</b>""",
        reply_to_message_id=message.message_id)
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🌹 𝗣𝗮𝗴𝗲𝘀 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝗡𝗲𝘅𝘁 ➡️ ",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🌹 𝗣𝗮𝗴𝗲𝘀 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⬅️ 𝗕𝗮𝗰𝗸", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🌹 𝗣𝗮𝗴𝗲𝘀 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⬅️ 𝗕𝗮𝗰𝗸", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("𝗡𝗲𝘅𝘁 ➡️", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🌹 𝗣𝗮𝗴𝗲𝘀 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("𝗡𝗲𝘅𝘁 ➡️", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🌹 𝗣𝗮𝗴𝗲𝘀 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⬅️ 𝗕𝗮𝗰𝗸", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("𝗡𝗲𝘅𝘁 ➡️", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🌹 𝗣𝗮𝗴𝗲𝘀 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [[
                InlineKeyboardButton('💠 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 💠', url='t.me/LatestMoviesHub001'),
                InlineKeyboardButton('💞 𝗗𝗲𝘃 💞', url="https://t.me/BKC0001")
                ],[
                InlineKeyboardButton('💠 𝗝𝗼𝗶𝗻 𝗚𝗿𝗼𝘂𝗽 💠', url=f'{TUTORIAL}')
                ]]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('♻️ 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 ♻️', url='t.me/joinchat/9Mq2rjj9YDk0YmZh'),
                    InlineKeyboardButton('♻️ 𝗝𝗼𝗶𝗻 𝗚𝗿𝗼𝘂𝗽 ♻️', url=f'{TUTORIAL}')
                ]
                ]
            await query.message.edit(text=f"{ABOUT}".format(TUTORIAL), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data.startswith("pr0fess0r_99"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('💠 𝗝𝗼𝗶𝗻 𝗚𝗿𝗼𝘂𝗽 💠', url=f'{TUTORIAL}')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("🥺𝗙𝗿𝗶𝗲𝗻𝗱.. 𝗧𝗵𝗮𝘁'𝘀 𝗡𝗼𝘁 𝗙𝗮𝗶𝗿 😓𝗣𝗹𝗲𝗮𝘀𝗲 𝗝𝗼𝗶𝗻 𝗧𝗵𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹..🥺",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('💠 𝗝𝗼𝗶𝗻 𝗚𝗿𝗼𝘂𝗽 💠', url=f'{TUTORIAL}')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("😁 𝗛𝗲𝘆 𝗙𝗿𝗶𝗲𝗻𝗱,𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝗿𝘀𝗲𝗹𝗳. 😁",show_alert=True)
