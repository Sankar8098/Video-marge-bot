import time
from pyrogram import filters, Client as mergeApp
from pyrogram.types import Message, InlineKeyboardMarkup
from helpers.msg_utils import MakeButtons
from helpers.utils import UserSettings


@mergeApp.on_message(filters.command(["settings"]))
async def f1(c: mergeApp, m: Message):
    # setUserMergeMode(uid=m.from_user.id,mode=1)
    replay = await m.reply(text="Please wait", quote=True)
    usettings = UserSettings(m.from_user.id, m.from_user.first_name)
    await userSettings(
        replay, m.from_user.id, m.from_user.first_name, m.from_user.last_name, usettings
    )


async def userSettings(
    editable: Message,
    uid: int,
    fname,
    lname,
    usettings: UserSettings,
):
    b = MakeButtons()
    if usettings.user_id:
        if usettings.merge_mode == 1:
            userMergeModeId = 1
            userMergeModeStr = "Video + Video"
        elif usettings.merge_mode == 2:
            userMergeModeId = 2
            userMergeModeStr = "Video + Audio"
        elif usettings.merge_mode == 3:
            userMergeModeId = 3
            userMergeModeStr = "Video + Subtitle"
        elif usettings.merge_mode == 4:
            userMergeModeId = 4
            userMergeModeStr = "Extract"
        if usettings.edit_metadata:
            editMetadataStr = "✅"
        else:
            editMetadataStr = "❌"
        uSettingsMessage = f"""
<b><u>🛠️ 𝙐𝙨𝙚𝙧 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 🛠️</u></b>

┏**👤 User:** <a href='tg://user?id={uid}'>{fname}</a>
┣**🆔 ID:** <code>{usettings.user_id}</code>
┣**🚷 Ban Status:** <code>{usettings.banned}</code>
┣**🚦 Allowed:** <code>{usettings.allowed}</code>
┣**📝 Edit Metadata:** <code>{usettings.edit_metadata}</code>
┗**Ⓜ️ Merge Mode:** <code>{userMergeModeStr}</code>

<a href="https://t.me/ACE_ML"><b>♥️ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 @𝗔𝗖𝗘_𝗠𝗟</b></a>
"""
        markup = b.makebuttons(
            [
                "📝 Edit Metadata »",
                editMetadataStr,
                "Ⓜ️ Merge Mode »",
                userMergeModeStr,
                "Close",
            ],
            [
                "tryotherbutton",
                f"toggleEdit_{uid}",
                "tryotherbutton",
                f"ch@ng3M0de_{uid}_{(userMergeModeId%4)+1}",
                "close",
            ],
            rows=2,
        )
        res = await editable.edit(
            text=uSettingsMessage, reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview=True
        )
    else:
        usettings.name = fname
        usettings.merge_mode = 1
        usettings.allowed = False
        usettings.edit_metadata = False
        usettings.thumbnail = None
        await userSettings(editable, uid, fname, lname, usettings)
    # await asyncio.sleep(10)
    # await c.delete_messages(chat_id=editable.chat.id, message_ids=[res.id-1,res.id])
    return
