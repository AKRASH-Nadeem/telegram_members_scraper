from pyrogram import Client, filters, idle
from pyrogram.enums import ChatType, ChatMemberStatus
import sqlite3
import sys


from config import session_string


con = sqlite3.connect("info.db", isolation_level=None,
                      check_same_thread=False)

if session_string == '' or session_string == None:
    print("Use create_session.py to add session first then run this program")
    sys.exit()

app = Client("my_account", session_string=session_string)


@app.on_message(filters.command(commands=['getgroups']) & filters.text & filters.me & filters.private)
async def scrap(client, message):
    try:
        await client.send_message("me", "Getting the groups please wait...")
        async for dialog in app.get_dialogs():
            if dialog.chat.type == ChatType.GROUP or dialog.chat.type == ChatType.SUPERGROUP:
                # print(dialog.chat.title)
                con.execute("INSERT OR IGNORE INTO groups(username,chatid,members_count) VALUES(?,?,?)", [
                            dialog.chat.username, dialog.chat.id, dialog.chat.members_count])
        con.commit()
        await client.send_message("me", "Got the groups\nReady to scrap members")
    except Exception as error:
        await client.send_message("error : " + str(error))


@app.on_message(filters.command(commands=['cleargroups']) & filters.text & filters.me & filters.private)
async def scrap(client, message):
    try:
        con.execute("DELETE FROM groups")
        con.commit()
        await client.send_message("me", "Cleared all groups")
    except Exception as error:
        await client.send_message("error : " + str(error))


@app.on_message(filters.command(commands=['status']) & filters.text & filters.me & filters.private)
async def scrap(client, message):
    try:
        numberofgroups = len(con.execute("SELECT * from groups").fetchall())
        await client.send_message("me", f"Number of groups : {numberofgroups}")
    except Exception as error:
        await client.send_message("error : " + str(error))


@app.on_message(filters.command(commands=['help']) & filters.text & filters.me & filters.private)
async def scrap(client, message):
    try:
        await client.send_message("me", "/getgroups : get the id of all groups in which you are joined\n/getmembers : get members username from all groups\n/cleargroups : clear the id of groups in database")
    except Exception as error:
        await client.send_message("error : " + str(error))


@app.on_message(filters.command(commands=['getmembers']) & filters.text & filters.me & filters.private)
async def scrap(client, message):
    await client.send_message("me", "Getting the groups members...")
    chats = con.execute("SELECT chatid,username FROM groups").fetchall()
    count = 0
    # async for member in client.get_chat_members(int(chats[0][0]), filter=ChatMembersFilter.BOTS):
    #     print(member)
    #     break
    me = await app.get_me()
    d = await app.send_message("me", f"Members : {count}")
    for chat in chats:
        with open("members.csv", "a") as fi:
            async for member in client.get_chat_members(int(chat[0])):
                if member.user.username:
                    if member.status == ChatMemberStatus.ADMINISTRATOR or member.status == ChatMemberStatus.OWNER or member.status == ChatMemberStatus.BANNED or member.user.id == me.id or member.user.is_bot:
                        continue
                    else:
                        fi.write(member.user.username + "\n")
                        count += 1
                        if count % 1000 == 0:
                            try:
                                await d.edit_text(f"Members : {count}")
                            except Exception as error:
                                print(str(error))
                                continue
                else:
                    continue

    print("done")
    try:
        await client.send_message("me", "Got all members")
        await client.send_message("me", f"Total members : {count}")
        await app.send_document("me", "members.csv")
    except Exception as error:
        print(str(error))
    # print("done")
    # count = await app.get_chat_members_count(chat)
    # print(count)


@app.on_message(filters.command(['send']))
async def getit(client, message):
    try:
        await app.send_document("me", "members.csv")
    except Exception as error:
        await client.send_message("me", f"error : {error}")
if __name__ == "__main__":
    app.start()
    app.send_message("me", "started")
    print("[*] scraper bot started...")
    idle()
    app.stop()
