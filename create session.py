# Session creator

from pyrogram import Client
import os

import sqlite3

# os.system('pip install --upgrade pip')
# os.system('pip install Pyrogram==1.2.20')


banner = """
                   _                                   _             
 ___  ___  ___ ___(_) ___  _ __     ___ _ __ ___  __ _| |_ ___  _ __ 
/ __|/ _ \/ __/ __| |/ _ \| '_ \   / __| '__/ _ \/ _` | __/ _ \| '__|
\__ \  __/\__ \__ \ | (_) | | | | | (__| | |  __/ (_| | || (_) | |   
|___/\___||___/___/_|\___/|_| |_|  \___|_|  \___|\__,_|\__\___/|_|   
                                                                     
"""
print(banner)
print("""String Generator. ==> Get Your Api Id & Api Hash From my.telegram.org and fill accordingly."""
      )
print("")
try:
    APP_ID = int(input("Enter APP ID - "))
    API_HASH = input("Enter API HASH - ")

    with Client(name='myaccount', in_memory=True, api_id=APP_ID, api_hash=API_HASH) as c:
        print("")
        print("This is your STRING_SESSION. Please Keep It safe.")
        print("")
        #c.storage.SESSION_STRING_FORMAT = ">B?256sQ?"
        session = c.export_session_string()
        c.send_message("me", f"`{session}`")
        with open("config.py", "w")as file:
            file.write(f"""
            session_string = "{session}"\n
            """)
        # print(session)
        print("added")
        print("\n\n\n")
except KeyboardInterrupt as error:
    print("stopped")

exit()
