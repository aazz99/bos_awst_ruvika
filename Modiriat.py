from rubpy import Client, Message, handlers, methods
from asyncio import run
from config import *
import requests
import markdown2
import requests
from bs4 import BeautifulSoup
import requests
import pyshorteners
from googletrans import Translator
from PIL import Image
import json
from concurrent.futures import ThreadPoolExecutor
import requests
import urllib.request
from re import findall, search
import re
from pyshorteners import Shortener
import requests
from random import choice
import random
from re import findall, search
from requests import get,post
from threading import Thread
import traceback
import json
import datetime
import asyncio
from rubpy import exceptions
from bs4 import BeautifulSoup
import requests, json, random, os, time, collections, openai
from asyncio import run, sleep , gather , ensure_future , create_task
silence_list = []
no_gifs = []
(
    warnings,
    admingg,
    num_warn,
    list_ban,
    list_vizhe,
    list_skot,
    start_bot,
    zed_link,
    filters,
    group,
    text_pasokh,
) = (
    ["00"],
    [],
    3,
    [],
    [],
    [],
    True,
    True,
    ["@", "http", ".ir"],
    [],
    ["عشقم😎😘", "زندگیم🥰❤", "نفسم💕😍", "عزیزم💋😊"],
)
class Locks:
    def __init__(self):
        self.locks = {
            "هوش مصنوعی": False,
            "حالت سخنگو": False,
            "خوشامد گویی": False,
            "اجرای بازی": False,
            "حالت ضدلینک": False,
            "حالت فروارد": False,
            "عمل حذف گیف": False,
            "قفل نظرسنجی": False,
            "عمل حذف ویس": False,
            "قفل لوکیشن": False,
            "عمل حذف عکس": False,
            "حالت ضدفیلم": False,
            "حالت ضدفایل": False,
            "حالت ضد لایو": False,
            "حالت ضد فحش": False,
            "قفل موزیک": False,
            "قفل روبینو": False,
        }
    def print_locks(self):
        locks_str = "نمایش وضعیت قفل‌ ها:\n"
        for key, value in self.locks.items():
            status = "(❌)" if value else "(✅)"
            locks_str += f"قفل ({key}) = ->{status}\n"  # تغییر این خط
        return locks_str
    
    def toggle_lock(self, lock_type):
        if lock_type in self.locks:
            self.locks[lock_type] = not self.locks[lock_type]
            status = "باز شده" if self.locks[lock_type] else "قفل شده"
            return f"قفل {lock_type} {status}"  # تغییر این خط
        else:
            return "نوع قفل معتبر نیست."
async def target(my_array, i: int, client: Client):
    await client.delete_messages(my_group, my_array[i : i + 30])
# خواندن کلمات و پاسخ‌ها از فایل کانفیگ
def load_sokhan():
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            sokhan_list = json.load(file)
            return sokhan_list
    except FileNotFoundError:
        return []

def save_sokhan(sokhan_list):
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(sokhan_list, file, ensure_ascii=False, indent=4)
def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, src='fa', dest='en')
    return translated.text
async def download_and_send_music(link, text_wbw, group_id, client: Client):
    try:
        response = requests.get(link)
        music_bytes = response.content
        file_name = "Music.mp3"
        with open(file_name, "wb") as f:
            f.write(music_bytes)
        print("Downloaded:", file_name)
        await client.send_voice(group_id, music_bytes, file_name="Music.mp3", caption=text_wbw)
    except Exception as e:
        print("Error:", e)

locks = Locks()
async def deleteMessages(client: Client, replay_message: str):
    try:
        messages_ids = []
        messages = await client.get_messages_interval(my_group, replay_message)
        while messages.old_has_continue:
            messages = await client.get_messages_interval(
                my_group, messages.old_max_id
            )
            for messeaged in messages.messages:
                messages_ids.append(messeaged.message_id)
        for i in range(0, len(messages_ids), 30):
            tasks = []
            task = ensure_future(target(messages_ids, i, client))
            tasks.append(task)
        await gather(*tasks)
        message_id = await client.send_message(
            my_group,
            f"تعداد {str(len(messages_ids))} پیام پاک شد !",
            replay_message,
        )
    except:
        message_id = await client.send_message(
            my_group,
            f"تعداد {str(len(messages_ids))} پیام پاک شد !",
            replay_message,
        )
async def main():
    async with Client(session="bot") as client:
        @client.on(handlers.MessageUpdates())
        async def updates(message: Message): 
            print(message.raw_text)
            global start_bot, warnings, text_wbw, zed_link, num_warn, look_gif, serch,tebchi, look_video, look_image, look_poll, look_fosh, look_music, look_file, look_live, look_location, look_hard, list_skot, look_voice, look_jock, look_danestani, look_bio, look_time, look_gpt
            msg = message.message_id
            req = message.author_guid
            if message.raw_text == "اد":
                await client.set_group_admin(my_group, req, access_list=[])  
                result = await client(methods.groups.GetGroupLink(my_group))
                result = result.to_dict().get('join_link')
                await client.send_message(req,f"♡**شما با موفقعیت اد شدید:white_check_mark:**♡\n\nلینک گروه\n{result}")
            if message.object_guid == my_group:
                req = await client.get_channel_all_members("c0BeTJ40e79f2113cb16f04e2314dadc")
                for member in req['in_chat_members']:
                    print(member['member_guid'])
                    if message.author_guid in member:
                        print("ok")
                print(message.raw_text)
                if message.raw_text and message.raw_text.startswith("برسی"):
                    text_wbw = message.text.split(":")[-1].strip()
                if message.raw_text and message.raw_text.startswith("اهنگ : "):
                    qe = message.author_guid
                    text_wbw = message.text.split(":")[-1].strip()
                    url = f"https://music-fa.com/search/{text_wbw}"
                    
                    try:
                        response = requests.get(url)
                        response.raise_for_status()  # Check for HTTP errors
                        soup = BeautifulSoup(response.content, "lxml")
                        
                        link = soup.find(attrs={"data-song": True})
                        if link:
                            print(link["data-song"])
                            
                            file_name = "Music.mp3"
                            response = requests.get(link["data-song"])
                            response.raise_for_status()  # Check for HTTP errors
                            
                            with open(file_name, "wb") as f:
                                f.write(response.content)
                            print("Downloaded:", file_name)
                            
                            music_bytes = response.content
                            await client.send_voice(qe, music_bytes, file_name="Music.mp3", caption=text_wbw,reply_to_message_id=msg)
                            await client.send_message(my_group,"نتایج کامل پیوی شما ارسال گردید",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"متاسفانه اهنگ درخواستی یافت نشد.",reply_to_message_id=msg)
                    except Exception as e:
                        await client.send_message(my_group,"متاسفانه اهنگ درخواستی یافت نشد.")
                        if message.author_guid in admins and message.raw_text == "بستن گروه":
                            await client.set_group_default_access(my_group, [])
                            await client.send_message(my_group,
                                                message='گروه بسته شد , جهت اد شدن در گروه به پیوی من کلمه **اد** رو بفرستید.',
                                                reply_to_message_id=msg)
                if message.author_guid in list_skot:
                    await message.delete_messages()
                    print("prints")
                if message.raw_text and message.raw_text.startswith("برجسته"):
                    req = message.reply_message_id
                    reg = await client.get_messages_by_ID(my_group, req)
                    
                    text_list = []
                    
                    for msg in reg['messages']:
                        text = msg['text']
                        text_list.append(text)
                        message_id = msg['message_id']
                        print(text)
                    await message.reply(f"متن برجسته شده:\n\n**{text}**")
                if message.raw_text and message.raw_text.startswith("تکی"):
                    req = message.reply_message_id
                    reg = await client.get_messages_by_ID(my_group, req)
                    
                    text_list = []
                    
                    for msg in reg['messages']:
                        text = msg['text']
                        text_list.append(text)
                        message_id = msg['message_id']
                        print(text)
                    await message.reply(f"متن تکی شده:\n\n**{text}**")
                if message.raw_text and message.raw_text.startswith("کج"):
                    req = message.reply_message_id
                    reg = await client.get_messages_by_ID(my_group, req)
                    
                    text_list = []
                    
                    for msg in reg['messages']:
                        text = msg['text']
                        text_list.append(text)
                        message_id = msg['message_id']
                        print(text)
                    await message.reply(f"متن کج شده:\n\n**{text}**")
                if message.raw_text and message.raw_text.startswith("هایپر"):
                    req = message.reply_message_id
                    reg = await client.get_messages_by_ID(my_group, req)
                    
                    text_list = []
                    
                    for msg in reg['messages']:
                        text = msg['text']
                        text_list.append(text)
                        message_id = msg['message_id']
                        print(text)
                        result = await client.get_user_info(message.author_guid)
                    await message.reply(f"متن هایپر شده:\n\n[{text_list}]({message.author_guid})")
                if message.raw_text and message.raw_text.startswith("نیم بها : "):
                    original_link = message.text.split(":")[-1].strip()
                    s = pyshorteners.Shortener()
                    short_link = s.tinyurl.short(original_link)
                    await client.send_message(my_group,f"لینک نیم بهای شما:\n\n{short_link}",reply_to_message_id=msg)
                if message.raw_text and message.raw_text.startswith("کرونا :"):
                    author_guidgg = message.author_guid
                    print(author_guidgg)
                    
                    # استخراج نام کشور از پیام
                    text_wbw = message.text.split(":")[-1].strip()
                    
                    # ترجمه نام کشور به انگلیسی
                    translated_country_name = translate_to_english(text_wbw)
                    
                    jd = requests.get(f"https://api.codebazan.ir/corona/?type=country&country={translated_country_name}").json()
                    
                    if jd["ok"]:
                        data = jd["result"]
                        
                        custom_key_names = {
                            "recovered": "تعداد بهبود یافتگان",
                            "deaths": "تعداد فوت شدگان",
                            "cases": "تعداد موارد",
                            "country": "نام کشور"
                        }
                        
                        result_text = ""  # متغیر جمع‌آوری کننده
                        
                        for key, custom_name in custom_key_names.items():
                            value = data.get(key)
                            result_text += f"{custom_name}: {value}\n"  # افزودن مقدار به متن جمع‌آوری کننده
                        
                        await client.send_message(my_group, f"|#𝕔𝕠𝕣𝕠𝕟𝕒\n==============\n{result_text}==============", reply_to_message_id=msg)
                if message.author_guid in admins and message.raw_text == "باز کردن گروه":
                    await client.set_group_default_access(my_group, ['SendMessages'])
                    await client.send_message(my_group,
                                                message='گروه باز شد.',
                                                reply_to_message_id=msg)
                if message.author_guid in admins and message.raw_text == "سکوت":
                    try:
                        if message.reply_message_id != None:
                            result = await client.get_messages_by_ID(
                                my_group, [message.reply_message_id]
                            )
                            result = result.to_dict()["messages"][0]
                            if not result["author_object_guid"] in admins:
                                if (
                                    not result["author_object_guid"]
                                    in list_vizhe
                                ):
                                    list_skot.append(
                                        result["author_object_guid"]
                                    )
                                    await client.send_message(
                                        my_group,"کاربر ساکت شد.",
                                        reply_to_message_id=msg
                                    )
                                else:
                                    await client.send_message(
                                        my_group,"کاربر یک فرد ویژه می باشد!",
                                        reply_to_message_id=msg
                                    )
                            else:
                                await client.send_message(
                                        my_group,"کاربر یک ادمین می باشد!",
                                        reply_to_message_id=msg
                                    )
                        else:
                            await client.send_message(
                                        my_group,"لطفا روی یک پیام رپلای کنید!",
                                        reply_to_message_id=msg
                                    )
                    except IndexError:
                        await client.send_message(
                                        my_group,"ظاهرا پیامی که روی آن ریپلای کرده اید پاک شده است.",
                                        reply_to_message_id=msg
                                    )
                elif message.raw_text == "لیست سکوت":
                    if list_skot != []:
                        collection = collections.Counter(list_skot)
                        list_text = ["لیست سکوت ها:\n"]
                        keys_collection = collection.keys()
                        for key_collection in keys_collection:
                            list_text.append(
                                f"\n [کاربر]({key_collection})"
                            )
                        list_text = " ".join(list_text)
                        await message.reply(list_text)
                    else:
                        await message.reply("لیست سکوت خالی است")
                if message.author_guid in admins and message.raw_text == "حذف سکوت":
                    try:
                        if message.reply_message_id != None:
                            result = await client.get_messages_by_ID(
                                my_group, [message.reply_message_id]
                            )
                            result = result.to_dict()["messages"][0]
                            if not result["author_object_guid"] in admins:
                                if (
                                    not result["author_object_guid"]
                                    in list_vizhe
                                ):
                                    list_skot.remove(
                                        result["author_object_guid"]
                                    )
                                    await client.send_message(
                                        my_group,"کاربر از لیست سکوت اومد بیرون.",
                                        reply_to_message_id=msg
                                    )
                    except IndexError:
                        await client.send_message(
                                        my_group,"ظاهرا پیامی که روی آن ریپلای کرده اید پاک شده است.",
                                        reply_to_message_id=msg
                                    )
                if message.author_guid in admins and message.raw_text == "بن":
                    try:
                        if message.reply_message_id != None:
                            result = await client.get_messages_by_ID(
                                my_group, [message.reply_message_id]
                            )
                            result = result.to_dict()["messages"][0]
                            if not result["author_object_guid"] in admins:
                                if (
                                    not result["author_object_guid"]
                                    in list_vizhe
                                ):
                                    try:
                                        user_guid = result[
                                            "author_object_guid"
                                        ]
                                        list_ban.append(user_guid)
                                        result = (
                                            await client.ban_group_member(
                                                my_group, user_guid
                                            )
                                        )
                                        result = await client.get_user_info(
                                            user_guid
                                        )
                                        await client.send_message(
                                            my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موفقیت حذف شد!",reply_to_message_id=msg
                                        )
                                    except exceptions.InvalidAuth:
                                        await client.send_message(
                                            my_group,"ربات ادمین نمی باشد",reply_to_message_id=msg
                                        )
                                else:
                                    await client.send_message(
                                            my_group,"ربات ادمین نمی باشد",reply_to_message_id=msg
                                        )
                            else:
                                await client.send_message(
                                            my_group,"کاربر یک ادمین میباشد!",reply_to_message_id=msg
                                        )
                        else:
                            await client.send_message(
                                            my_group,"لطفا روی یک پیام رپلای کنید!",reply_to_message_id=msg
                                        )
                    except exceptions.InvalidAuth:
                        await client.send_message(
                                            my_group,"ظاهرا پیامی که روی آن ریپلای کرده اید پاک شده است.",reply_to_message_id=msg
                                        )
                if message.author_guid in admins and message.raw_text == "حذف بن @":
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                result = (
                                    await client.unban_group_member(
                                        my_group, user_guid
                                    )
                                )
                                result = await client.get_user_info(
                                    user_guid
                                )
                                await client.send_message(my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موفقیت از لیست بن بیرون امد شد",reply_to_message_id=msg)
                            
                elif message.author_guid in admins and message.raw_text == "بن @":
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                if not user_guid in admins:
                                    if not user_guid in list_vizhe:
                                        try:
                                            list_ban.append(user_guid)
                                            result = await client.ban_group_member(
                                                my_group, user_guid
                                            )
                                            result = (
                                                await client.get_user_info(
                                                    user_guid
                                                )
                                            )
                                            await client.send_message(my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موفقیت حذف شد",reply_to_message_id=msg)
                            
                                        except exceptions.InvalidAuth:
                                            await client.send_message(my_group,"ربات ادمین نمی باشد",reply_to_message_id=msg)
                                    else:
                                        await client.send_message(my_group,"کاربر در لیست افراد ویژه میباشد!",reply_to_message_id=msg)
                                else:
                                    await client.send_message(my_group,"کاربر در لیست افراد ویژه میباشد!",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                    else:
                        await client.send_message(my_group,"آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                elif message.raw_text == "لیست بن":
                    if list_ban != []:
                        collection = collections.Counter(list_ban)
                        list_text = ["لیست بن ها:\n"]
                        keys_collection = collection.keys()
                        for key_collection in keys_collection:
                            list_text.append(
                                f"\n [کاربر]({key_collection})"
                            )
                        list_text = " ".join(list_text)
                        await message.reply(list_text)
                    else:
                        await message.reply("لیست بن خالی است")
                elif message.author_guid in admins and message.raw_text == "حذف بن":
                    try:
                        if message.reply_message_id != None:
                            result = await client.get_messages_by_ID(
                                my_group, [message.reply_message_id]
                            )
                            result = result.to_dict()["messages"][0]
                            if not result["author_object_guid"] in admins:
                                if (
                                    not result["author_object_guid"]
                                    in list_vizhe
                                ):
                                    try:
                                        user_guid = result[
                                            "author_object_guid"
                                        ]
                                        result = (
                                            await client.unban_group_member(
                                                my_group, user_guid
                                            )
                                        )
                                        result = await client.get_user_info(
                                            user_guid
                                        )
                                        await client.send_message(
                                            my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موفقیت از لیست سیاه برکنار شد!",reply_to_message_id=msg
                                        )
                                    except exceptions.InvalidAuth:
                                        await client.send_message(
                                            my_group,"ربات ادمین نمی باشد",reply_to_message_id=msg
                                        )
                                else:
                                    await client.send_message(
                                            my_group,"ربات ادمین نمی باشد",reply_to_message_id=msg
                                        )
                            else:
                                print("ok")
                        else:
                            await client.send_message(
                                            my_group,"لطفا روی یک پیام رپلای کنید!",reply_to_message_id=msg
                                        )
                    except exceptions.InvalidAuth:
                        await client.send_message(
                                            my_group,"ظاهرا پیامی که روی آن ریپلای کرده اید پاک شده است.",reply_to_message_id=msg
                                        )
                if message.author_guid in admins and message.raw_text == "سکوت":
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                if not user_guid in admins:
                                    if not user_guid in list_vizhe:
                                        admins.append(user_guid)
                                        result = await client.get_user_info(
                                            user_guid
                                        )
                                        await client.send_message(my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موقفیت به لیست افراد ویژه افزوده شد",reply_to_message_id=msg)
                                    else:
                                        await client.send_message(my_group,"کاربر مورد نظر در لیست افراد ویژه میباشد.",reply_to_message_id=msg)
                                else:
                                    await client.send_message(my_group,"کاربر مورد نظر در گروه ادمین می باشد.",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"کاربر مورد نظر در گروه ادمین می باشد.",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                    else:
                        await message.reply("آیدی مورد نظر اشتباه می باشد.")
                elif message.author_guid in admins and message.raw_text.startswith("حذف سکوت @"):
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                if user_guid in list_skot:
                                    list_skot.remove(user_guid)
                                    await client.send_message(my_group,"کاربر با موفقیت از لیست سکوت بیرون امد",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"آیدی مورد نظر اشتباه است.",reply_to_message_id=msg)
                    else:
                        await client.send_message(my_group,"آیدی مورد نظر اشتباه است.",reply_to_message_id=msg)
                elif message.author_guid in admins and message.raw_text.startswith("افزودن ویژه @"):
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                if not user_guid in admins:
                                    if not user_guid in list_vizhe:
                                        admins.append(user_guid)
                                        result = await client.get_user_info(
                                            user_guid
                                        )
                                        await client.send_message(my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موقفیت به لیست افراد ویژه افزوده شد",reply_to_message_id=msg)
                                    else:
                                        await client.send_message(my_group,"کاربر مورد نظر در لیست افراد ویژه میباشد.",reply_to_message_id=msg)
                                else:
                                    await client.send_message(my_group,"کاربر مورد نظر در گروه ادمین می باشد.",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"!آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                    else:
                        await client.send_message(my_group,"آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                if message.author_guid in admins and message.raw_text == "حذف ویژه @":
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                if not user_guid in admingg:
                                    if user_guid in list_vizhe:
                                        admins.remove(
                                        result["author_object_guid"]
                                        )
                                        result = await client.get_user_info(
                                            user_guid
                                        )
                                        await client.send_message(my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موقفیت به لیست افراد ویژه حذف شد",reply_to_message_id=msg)
                                        await message.reply(
                                            
                                        )
                                    else:
                                        await client.send_message(my_group,"کاربر مورد نظر در لیست افراد ویژه میباشد.",reply_to_message_id=msg)
                                        await message.reply(
                                            
                                        )
                                else:
                                    await client.send_message(my_group,"کاربر مورد نظر در گروه ادمین می باشد.",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"!آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                    else:
                        await client.send_message(my_group,"آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                elif message.author_guid in admins and message.raw_text.startswith("حذف ویژه"):
                    username = message.text.split("@")[-1]
                    if username != "":
                        result = await client.get_object_by_username(
                            username.lower()
                        )
                        result = result.to_dict()
                        if result.get("exist"):
                            if result.get("type") == "User":
                                user_guid = result.get("user").get(
                                    "user_guid"
                                )
                                if not user_guid in admins:
                                    if user_guid in list_vizhe:
                                        list_vizhe.remove(user_guid)
                                        result = await client.get_user_info(
                                            user_guid
                                        )
                                        await client.send_message(my_group,f"کاربر [{result.user.first_name}]({user_guid}) با موقفیت به لیست افراد ویژه حذف شد",reply_to_message_id=msg)
                                    else:
                                        await client.send_message(my_group,"کاربر مورد نظر در لیست افراد ویژه میباشد.",reply_to_message_id=msg)
                                else:
                                    await client.send_message(my_group,"کاربر مورد نظر در گروه ادمین می باشد.",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"کاربر مورد نظر کاربر عادی نیست.",reply_to_message_id=msg)
                        else:
                            await client.send_message(my_group,"!آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                    else:
                        await client.send_message(my_group,"آیدی مورد نظر اشتباه می باشد.",reply_to_message_id=msg)
                        await message.reply()
                elif message.raw_text == "لیست ویژه":
                    if admins != []:
                        collection = collections.Counter(admins)
                        list_text = ["لیست ویژه ها:\n"]
                        keys_collection = collection.keys()
                        for key_collection in keys_collection:
                            list_text.append(
                                f"\n [کاربر]({key_collection})"
                            )
                        list_text = " ".join(list_text)
                        await message.reply(list_text)
                    else:
                        await message.reply("لیست ویژه خالی است")
                if message.author_guid in admins and message.raw_text == "لیست قفل" or message.raw_text == "/LOCKS":
                    locks_str = "وضعیت قفل‌ها:\n"
                    max_key_length = max(len(key) for key in locks.locks)
                    for key, value in locks.locks.items():
                        status = "(✅)" if value else "(🔐)"
                        formatted_key = key.capitalize()
                        locks_str += f"قفل ({formatted_key.ljust(max_key_length, ' ')}) -> {status}\n"
                    await client.send_message(my_group,locks_str,reply_to_message_id=msg)
#await Client.get_poll_status
#await Client.get_poll_option_voters
#await Client.vote_poll
#await Client.create_poll
                if message.raw_text is not None and message.author_guid in admins and message.raw_text.startswith(("قفل ", "بازکردن ")):
                    parts = message.raw_text.split(" ", 1)
                    if len(parts) == 2:
                        action, lock_type = parts
                        lock_type = lock_type.lower()
                        if action == "بازکردن":
                            if lock_type == "سختگیرانه":
                                for key in locks.locks:
                                    locks.locks[key] = True
                                await client.send_message(my_group,"تمام قفل‌ها باز شدند.",reply_to_message_id=msg)
                            elif lock_type in locks.locks:
                                locks.locks[lock_type] = True
                                formatted_lock_type = lock_type.capitalize()
                                await client.send_message(my_group,f"قفل {formatted_lock_type} باز شد.",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"نوع قفل معتبر نیست.",reply_to_message_id=msg)
                        elif action == "قفل":
                            if lock_type == "سختگیرانه":
                                for key in locks.locks:
                                    locks.locks[key] = False
                                await client.send_message(my_group,"تمام قفل‌ها فعال شدند.",reply_to_message_id=msg)
                            elif lock_type in locks.locks:
                                locks.locks[lock_type] = False
                                formatted_lock_type = lock_type.capitalize()
                                await client.send_message(my_group,f"قفل {formatted_lock_type} بسته شد.",reply_to_message_id=msg)
                            else:
                                await client.send_message(my_group,"نوع قفل معتبر نیست.",reply_to_message_id=msg)
                if message.raw_text and message.raw_text.startswith("یک پیام سنجاق شد."):
                    await message.delete_messages()
                    result = message.to_dict().get("message")
                    if locks.locks["هوش مصنوعی"] == True:
                        if message.raw_text and message.raw_text.startswith("//"):
                            message_id = message.message_id
                            text_wb = message.text.split("//")[-1]
                            response = requests.get(f"https://haji-api.ir/Free-GPT3/?text={text_wb}&key=hajiapi")
                            data = response.json()
                            message = data["result"]["message"]
                            await client.send_message(my_group,message,reply_to_message_id=message_id)
                if message.author_guid in admins and message.raw_text == "دستورات":
                    print("ok")
                    await client.send_message(my_group,"""
                                            💠 | ᑭᗩᑎᗴᒪ: 

/SETTING လ تنظیمات

/CONDITION လ وضعیت

/LOCKS လ لیست قفل

/GAMES လ بازی
‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‌‌
                                            """,reply_to_message_id=msg)
                if message.author_guid in admins and message.raw_text == "/SETTING" or message.raw_text == "تنظیمات":
                    await client.send_message(my_group,"""
1️⃣ قفل و باز کردن :
📝با ارسال دستور اول گروه باز و با دستور دوم گروه بسته میشود
‎ᴥ باز کردن گروه
‎ᴥ قفل گروه
    ─┅━━━━┅─
2️⃣ پاکسازی گروه:
📝با ارسال این دستور ربات تمامی پیام های گروه رو حذف میکنه
‎ᴥ پاکسازی
─┅━━━━┅─
""",reply_to_message_id=msg)
                if message.author_guid in admins and message.raw_text == "وضعیت" or message.raw_text == "/CONDITION":
                    await client.send_message(my_group,'پلن یک ماهه برای شما فعال است |💠',reply_to_message_id=msg)
                if message.raw_text == "بازی" or message.raw_text == "/GAMES":
                    await client.send_message(my_group,"""
1️⃣ ارسال جوک , بیو , دانستنی:
📝با ارسال کلمات بالا ربات براتون میفرسته
‎ᴥ جوک
‎ᴥ بیو
‎ᴥ دانستنی
‎ᴥ بیو
─┅━━━━┅─
2️⃣ارسال ساعت در گروه :
📝 با ارسال کلمه ساعت ربات ساعت رو برای شما ارسال میکنه
‎ᴥ ساعت
─┅━━━━┅─
3️⃣ ترجمه به فارسی و اینگلیسی:
📝 با این دستور میتونید متنتون رو به فارسی یا اینگلیسی ترجمه کنید
‎ᴥ ترجمه به انگلیسی : متنتون فارسیتون رو بنویسید
‎ᴥ ترجمه به فارسی : متنتون فارسیتون رو بنویسید
─┅━━━━┅─
4️⃣ ترجمه به فارسی و اینگلیسی:
📝 با این دستور میتونید متنتون رو به فارسی یا اینگلیسی ترجمه کنید
‎ᴥ ترجمه به انگلیسی : متنتون فارسیتون رو بنویسید
‎ᴥ ترجمه به فارسی : متنتون فارسیتون رو بنویسید
─┅━━━━┅─
5️⃣ نمایش اوقات شرعی شهرتون :
📝 با این قابلیت میتونید اقات شرعی شهرتون رو دریافت کنید
‎ᴥ اوقات شرعی : اسم شهرتون
─┅━━━━┅─
6️⃣ ساخت فونت برای اسمتون :
📝 با این قابلیت میتونی برای اسمتون فونت بسازید
‎ᴥ فونت : متن فونتتون""",reply_to_message_id=msg)
                if locks.locks["اجرای بازی"] == True:
                    if message.author_guid in admins and message.raw_text == "ایجاد کال":
                        await client.create_voice_call(my_group)
                        await client.send_message(my_group,"کال با موفقعیت ایجاد شد.",reply_to_message_id=msg)
                    if message.raw_text == "دانستنی":
                        rando = ["شمپانزه ها قادرند مقابل آينه چهره خود را تشخيص دهند اما ميمونها نميتوانند.","فیلها قادرند روزانه ۶۰ گالن آب و ۲۵۰ کیلو گرم یونجه مصرف کنند.","سوسكها سريعترين جانوران 6 پا ميباشند. با سرعت يك متر در ثانيه.","وقتی موش ها را قلقلک بدهید میخندند.","بلژیک تنها کشوری است که فیلمهای غیر اخلاقی را سانسور نمیکند.","آیا میـدانستیـد کـه در ماکارونی 20درصد گنوتن صنعتی استفاده می شود که سرطان زاست و در بسیاری کارخانه ها نان خشک کپک زده به جای آرد در ماکارونی استفاده می شود و ماکارونی یبوست زاست ؟","چطوری رشد ابرو ها رو زیاد و تارهای ابرو رو ضخیم کنیم؟ رشد سریع ابرو 👈 دوبار روغن زیتون در روز ضخیم کردن تارهای ابرو 👈 استفاده از وازلین 👌😎","سطح شهر مكزيك سالانه 25 سانتي متر نشست ميكند.","تمامی پستانداران به استثنای انسان و میمون کور رنگ میباشند.","نور خورشيد 8.5 دقيقه طول ميكشد تا به زمين برسد.","اگر يک ماهي قرمز را در يک اتاق تاريک قرار دهيد، کم کم رنگش سفيد ميشود.","دکتر ها در ژاپن یک مغز کوچک را هنگام جراحی تومور تخمدان یک دختر ۱۶ ساله از آن خارج کردند.","صدای ” مومو ” گاو ها در کشورهای مختلف جهان با هم متفاوت است، آنها لهجه های خاص خود را دارند درست مثل انسان.","شما می توانید جنسیت یک اسب را با شمارش تعداد دندان های او تشخیص دهید، بیشتر اسب های جنس نر 40 دندان و اسب های جنس ماده 36 دندان دارند.","70درصد فقراي جهان را زنان تشكيل ميدهند.","در قرن ۱۶ در اروپا اعتقاد بر این بود که خوردن گوجه فرنگی میتواند شما را تبدیل به گرگ کند","کادمیم فلزی سمی است که در ساخت باطری های خشک کاربرد دارد","شيشه در ظاهر جامد به نظر ميرسد ولي در واقع مايعي است که بسيار کند حرکت ميکند.","چطوری مانع رنگ پریدگی لباس های مشکی در شستسو بشیم؟🤔 کافیه 👈 در تشتی یک فنجان سرکه + مایع لباس شویی + اب سرد + کمی مایع ظرفشویی نیم ساعت خیس بخورد سپس با دست لباس را بشویید","ون گوگ در طول حيات خود تنها يكي از نقاشيهاي خود را بفروش رساند.","تمامی خرسهای قطبی چپدست هستند.","يك اسب در طول يك سال 7 برابر وزن بدن خود غذا مصرف ميكند.","كرگدنها قادرند سريعتر از انسانها بدوند.","در سال ۲۰۰۸، پلیس بریتانیا به یک کودک ۷ ساله مجوز حمل اسلحه داد.","سگهاي شهري بطور متوسط 3 سال بيشتر از سگهاي روستايي عمر ميكنند.","آیا میـدانستیـد کـه ماده مخدری به نام cola (پپسی کولا، کوکا کولا و…) در اکثر نوشابه ها وجود دارد که کافئین و کارامل از این دست هستند ؟","انسانها قبل از اینکه زیر چمدان ها چرخ بزارن، یک نفر را روی ماه گذاشتند!","روزانه حدود ۱۵۳۰۰۰ نفر در جهان می‌میرند.","خودروسازي بزرگترين صنعت در جهان ميباشد.","آیا میـدانستیـد کـه گوشت گاو به گفته بوعلی سینا عامل 16 بیماری مهلک می باشد که اولین آن سرطان و دومین آن مالیخولیا (اسکیزوفرنی) و سومی آن بواسیر می باشد. جنون گاوی ویروس و میکروب نیست بلکه نوعی پروتئین گاو است","آیا میـدانستیـد کـه گوشت گاو به گفته بوعلی سینا عامل 16 بیماری مهلک می باشد که اولین آن سرطان و دومین آن مالیخولیا (اسکیزوفرنی) و سومی آن بواسیر می باشد. جنون گاوی ویروس و میکروب نیست بلکه نوعی پروتئین گاو است","فقط پشه های ماده خون میخورند، پشه های نر گیاه خوار هستند.","جویدن آدامس در سنگاپور ممنوع است.","حلزون های بی صدف 4 بینی دارند!","تیولا یا عروس دریایی نامیرا، تنها موجودی شناخته شده است که زندگی جاودانه دارد.","98 درصد وزن آب از اكسيژن تشكيل يافته است.","مرده ها هم موهای تنشان سیخ میشود(مور مور و اینا)","چطوری مانع رنگ پریدگی لباس های مشکی در شستسو بشیم؟🤔 کافیه 👈 در تشتی یک فنجان سرکه + مایع لباس شویی + اب سرد + کمی مایع ظرفشویی نیم ساعت خیس بخورد سپس با دست لباس را بشویید","آیا میـدانستیـد کـه گوشت مرغ و ماهی که متاسفانه سفارش بسیاری از پزشکان است بلغم زاست و موجب سکته و تومور های مختلف می گردند ؟","حس چشایی پروانه ها در پاهای شان می باشد","سگهاي شهري بطور متوسط 3 سال بيشتر از سگهاي روستايي عمر ميكنند.","باقیمانده پیاز رو داخل یخچال قرار ندهید!🤔 پیاز نصف شده به دلیل اینکه پوستی ندارد باکتری های یخچال رو به خود جذب میکند میتونید باقی مانده رو درجایی خشک و خنک نگه دارید👌😎","شرکت کوکا کولا روزانه بیش از 1 میلیارد از محصولات خود را به فروش می رساند.","یک هتل در بولیوی وجود دارد که بطور کامل از نمک ساخته شده، حتی تخت ها و صندلی هایش!","عمر تمساح بيش از 100 سال ميباشد.","آیا میـدانستیـد کـه در نان باگت برای متخلخل شدن از پودرهای بکینگ یا جوش شیرین زیاد استفاده می شود که در گمرک ها با علامت مرگ وارد میشود ؟","آیا میـدانستیـد کـه در نان باگت برای متخلخل شدن از پودرهای بکینگ یا جوش شیرین زیاد استفاده می شود که در گمرک ها با علامت مرگ وارد میشود ؟","ختنه کردن در قرون وسطی به عنوان درمانی برای فتق، صرع و جذام مورد استفاده قرار میگرفت.","مادر و همسر گراهام بل مخترع تلفن هر دو ناشنوا بوده اند.","آیا می دانستید هنگامی که عطسه می کنید، قلب شما برای یک میلی ثانیه متوقف می شود.","سگهاي شهري بطور متوسط 3 سال بيشتر از سگهاي روستايي عمر ميكنند.","اگر پلیس های تایلندی قانون شکنی کنند باید یک بازوبند کیتی ببندند.","لئوناردو داوينچي مخترع قيچي ميباشد.","جغدها قادر به حركت دادن چشمان خود در كاسه چشم نميباشند.","موز پر مصرف ترين ميوه كشور امريكا ميباشد.","کانگرو های ماده ۳ واژن دارند.","آیا میـدانستیـد کـه در نان باگت برای متخلخل شدن از پودرهای بکینگ یا جوش شیرین زیاد استفاده می شود که در گمرک ها با علامت مرگ وارد میشود ؟","ون گوگ در طول حيات خود تنها يكي از نقاشيهاي خود را بفروش رساند.","ون گوگ در طول حيات خود تنها يكي از نقاشيهاي خود را بفروش رساند.","اگر پلیس های تایلندی قانون شکنی کنند باید یک بازوبند کیتی ببندند.","گوسفند ها میتوانند همدیگر را در عکس تشخیص بدهند.","درتمام انسانهای کره زمین ۹۹٫۹ % شباهت ژنتیکی وجود دارد."]
                        renn= choice(rando)
                        await client.send_message(my_group,renn,reply_to_message_id=msg)
                    if message.raw_text == "جوک":
                        jd = requests.get("http://api.codebazan.ir/jok/").text
                        await client.send_message(my_group,jd,reply_to_message_id=msg)
                if message.raw_text == "بیو" or message.raw_text == "بیوگرافی":
                    rando = ["اگر از بلندای آسمان بترسی، نمی‌توانی مالکِ ماه شوی! 🌖✨ ️ ","༺ زندگے ات یـک قصـہ ایـست کـہ توسط یـک خداے خوب نوشتـہ شده! ༻️ ","ناشنوا باش وقتی کهـ به آرزوهای قشنگت میگن محالهـ💘🍀✨  ️ ","👑پادشاه جهنم خودت باش نه کارگر بهشت دیگران👑 #سنگین ️ "," «‌ترجیح میدهم به ذوقِ خویش دیوانه باشم تا به میلِ دیگران عاقل...» زندگی یعنی همین! ️ "," ♡ ♡ ربنا آتنا بغلش آرامشنا ♡ ‌ ‌◉━━━━━━─────── ↻ㅤ ◁ㅤㅤ❚❚ㅤㅤ▷ㅤㅤ⇆️ ","از هرجا بیوفتے ڪمڪت میڪنم بلند شی،هرجا جز چشمام! ️ ","همیشه به قلبت گوش بده درسته که طرف چپ بدنته، ولی همیشه راستشو میگه ♥️ ️ ","زشتی دنیا به خاطر وجود آدمای بد نیست ! به خاطر سکوت آدمای خوبه ...  ️ ","هیچ‌کس‌نفهمیدِꔷ͜ꔷ▾‹🖤⃟🌻›' که‌خداوندهمِꔷ͜ꔷ▾‹🥀⃟🕸›' تـــــنـهاییـش‌رافریادزدِꔷ͜ꔷ▾‹🔞⃟🌙›' _قُل‌هُوَاللّهُ‌اَحَدِꔷ͜ꔷ▾‹💔⃟🌿›' ️ ","بِدون‌ِتـومَگِه‌میشِه‌زِندِگی‌ڪَرد∘ ️ ","از دریا اموختم🌹هر کس از حدش گذشت غرقش کنم😍 ️ ","بخند، شایسته‌ی ماه نیست که غمگین باشه ⚠️♥️ ️ ","بخند، شایسته‌ی ماه نیست که غمگین باشه ⚠️♥️ ️ ","مرگ درمانیست برای اتمام درد زندگی ... و اکنون ، درمانم ارزوست ...🖤🥀🕸 ️ "," از گوش دادن به یه مشت حرف دروغ لذت می‌برم، وقتی‌که حقیقت رو می‌دونم... ️ ","گَر نباشد رنگِ رویا به چه دِل باید سِپرد :)؟! ️ ","آرزویت را برآورد میکند ، آن خدایی که آسمان را برای خنداندن گلی میگریاند . . . ️ ","تنها کسی که نگاهش کردم |تو| بودی من بقیه رو فقط میبینم . . 🌙♥️• ️ ","☘  روزهای سخت قیمت آدمای دورتو معلوم میکنه! 🔥☝️   ️ ","'خوشبَختی' یَعنی : ‌بُـودنش بهترین 'شانسِ' زنـدگیتـه..♥️ ️ ","‹ قوی باش ، چون خدا فقط کسی رو به لبه پرتگاه میرسونه که ؛ قدرت پرواز رو داشته باشه ... › ️ ","•|چـرا ایـن نیـز دیـگر نـِمـیـگـذَرَد ..:)؟• ️ ","ز گیتی دو کس را سپاس...یکی حق شناس و یکی حد شناس :) 🍃🌸 ️ ","نامه‌ای به خودم: الان دیگه فقط تورو دارم مراقبم باش :)    ️ ","  حواست به این باشه که وقتی خوشحالی کی برات خوشحاله!  ️ ","♛ خیلیا بهم یاد دادن که میتونن باهام بازی کنن.♛ 彡منم یه روز بهشون یاد میدم که بازی رفت و برگشت داره彡️ ","اگر دیدی کسی از تنهایش لذت میبره؛ بدون راز قشنگی تو دلش داره...🖤 و اگه تونستی حریم این تنهایی رو بشکنی بدون تو از رازش قشنگ تری...🙂 ️ ","   من عشق‌رو آرزو کردمو تو مستجاب شدی..!🦋 ️ ","این کلمه‌ها زندگی من هستن: مامان و بابام♥️ ️ ","هیچ گونه از زیبایی درخشان‌تر از «یه قلب پاک» نمی‌درخشد. ✨ ️ ","عاشقت که شدم:  عقلم کیش شد، قلبم مات❤️ ️ ","پـــــــــــرواز کن تا آرزو 😉✈️ زنجیــــر را بــــــاور نکن ⛓✨ ️ ","پـــــــــــرواز کن تا آرزو 😉✈️ زنجیــــر را بــــــاور نکن ⛓✨ ️ ","نگران حرف مردم نباش خدا پرونده ای را که مردم مینویسند    نمیخواند... ️ ","⌈ دَر دِلِ بینَوایِ مَن عِشقِ تُو چَنگ می‌زَنَد!❤️🔗 ⌋ ️ ","اگه سکوت میکنم معنیش این نیست که دارم حق رو به تو میدم بلکه به سادگی دارم تورو نادیده میگیرم :) ️ ","به سݪاݥتے ڱڔگے ڪع تا فهݥید چؤپان خؤاب است باز زؤزه اش را ڪشید تا از پشت خنجڔ نزند 😊😍 ️ ","‌‌🌿 میشه‌ از‌ وُیسات‌ قرص‌ِ آرامبَخش‌ساخت..🎼 . ️ ","چیز‌هایی که می‌شنوی رو زود باور نکن چون دروغ‌ها سریعتر از حقیقت پخش می‌شن :)) ️ ","  راضی باش به رضای او... 👤 سوره طور ️ ","ذهنای بزرگ پُراز هدف هستن، ذهنای کوچیک پراز آرزو! ️ ","ذهنای بزرگ پُراز هدف هستن، ذهنای کوچیک پراز آرزو! ️ ","‌‌‌‌🌿 انقلاب، فقـط لبخنـدش..! (:  ‌‌‌‌ ️ ","هیچ کسی از داستان کسی دیگه خبر نداره؛ درد یک سُفره‌ی تک نفرست ️ ","باب اسفنجی:میدونی هرچی مشکل دارم از سادگیمه.. پاتریک:دیگه ساده نباش؛راه راه باش:)‌ ️ ","اندوهت را بتکان،جهان منتظرت نمی ماند تا حالت خوب شود🌿💛 ️ "," - اﻧﻗَﺩࢪ ﻧﮔࢪﺩ ﺩﻧﺑالِ اﻭنے ﻛِ‌‍ہ اﺯ ﻗَﺻﺩ ﮔﻣِﺗ ﻛࢪدِ‍‌؏..!'•ᤩ😹➰  ‌‌‌‌‌ ️ ","تو متعلق به غم و اندوه نیستی؛ بی‌خیال اون چیزی شو که روی قلبت سنگینی می‌کنه ✨ ️ ","به هرکس می‌نگرم در شکایت است : در حیرتم که لذت دنیا به کام کیست ؟! ️ "," وقتی یه دختر جوری رفتار میکنه که انگار بهت اهمیت نمیده ، اون موقع‌ست که بیشتر از همیشه بهت احتیاج داره . ️ ","•فِكرایِ توْ سَرَم اَز هَنزفِريم پيچيدِه تَرَن♥️ ","تو اون بخشی از وجود منی که هرگز نمی‌میره♡ ️ ","هیچ لباسی تو دنیا، نمیتونه بی‌شخصیتیه درون آدما رو بپوشونه👌 ️ ","دکتر انوشه راست میگه که : 'گیرم عذر خواهی کردی ، واسه حرفی که زدی' با ذاتی که آشکار شده چه میکنی ؟! ️ ","برات اشک آرزو می‌کنم! نه در اوج غم، در اوج خنده …💛 ️ ","با نگاه کردن به گذشته وقت تلف نکن. به اون سمت نمیری🌹 ️ ","وقتی چیزی تموم شد، ترکش کن به آبیاری یه گل مرده ادامه نده ️ "," بعضی از آدما عین ریشه می‌مونن، باعث می‌شن قوی و استوار باشی 🌱 ️ ","خدا یاری‌ کند قلبی را که  در آرزوی چیزیست که تقدیرش نیست  ️ ","‏‌ انسانها همه چیو نابود میکنند، پنهان زندگی کن‌ ! ️ ","آنجا که گلها شکوفه میکنند ، اُمید حضور دارد . .💛🌻 ️ ","آنجا که گلها شکوفه میکنند ، اُمید حضور دارد . .💛🌻 ️ "]
                    renn= choice(rando)
                    await client.send_message(my_group,renn,reply_to_message_id=msg)
                if message.raw_text == "ساعت" or message.raw_text == "تایم":
                    jd = requests.get("http://api.codebazan.ir/time-date/?td=time").text
                    await client.send_message(my_group,f"گلم ساعت **{jd}** هست",reply_to_message_id=msg)
                
                if message.raw_text and message.raw_text.startswith("فونت :"):
                    author_guidgg = message.author_guid
                    print(author_guidgg)
                    text_wbw = message.text.split(":")[-1].strip()
                    responsew = requests.get(f"https://api.codebazan.ir/font/?text={text_wbw}")
                    jokgw = responsew.text
                    jdw = json.loads(jokgw)['result']
                    resultw = [f"{i}. {jdw[str(i)]}" for i in range(1, 101) if str(i) in jdw]
                    await client.send_message(author_guidgg,'\n'.join(resultw))
                    await message.reply("🔷 نتایج کامل به پیوی شما ارسال گردید 🔷")

                if message.raw_text and message.raw_text.startswith("فونت فارسی : "):
                    author_guidgge = message.author_guid
                    text_wbq = message.text.split(":")[-1].strip()
                    responseq = requests.get(f"https://api.codebazan.ir/font/?type=fa&text={text_wbq}")
                    jokeq = responseq.text
                    jdq = json.loads(jokeq)['Result']
                    resultq = [f"{i}. {jdq[str(i)]}" for i in range(1, 10) if str(i) in jdq]
                    await client.send_message(author_guidgge,'\n'.join(resultq))
                    await message.reply("🔷 نتایج کامل به پیوی شما ارسال گردید 🔷")

                if message.raw_text and message.raw_text.startswith("ربات کی"):
                    result = await client.get_group_all_members(my_group)
                    jd = json.loads(str(result))  # تبدیل نتیجه به رشته و سپس به دیکشنری
                    in_chat_members = jd['in_chat_members']
                    first_names = [member.get('first_name', '') for member in in_chat_members if 'first_name' in member]
                    if first_names:
                        random_first_name = random.choice(first_names)
                        print(random_first_name)  # نمایش نام تصادفی
                        await message.reply(f"فکر کنم {random_first_name}")
                if message.raw_text and message.raw_text.startswith("رباط کی"):
                    result = await client.get_group_all_members(my_group)
                    jd = json.loads(str(result))  # تبدیل نتیجه به رشته و سپس به دیکشنری
                    in_chat_members = jd['in_chat_members']
                    first_names = [member.get('first_name', '') for member in in_chat_members if 'first_name' in member]
                    if first_names:
                        random_first_name = random.choice(first_names)
                        print(random_first_name)  # نمایش نام تصادفی
                        await message.reply(f"فکر کنم {random_first_name}")
                if message.raw_text and message.raw_text.startswith("ترجمه به فارسی : "):
                    text_wb = message.text.split(":")[-1]
                    response = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={text_wb}")
                    data = json.loads(response.text)
                    text = data['result']
                    await message.reply(text)
                if message.raw_text and message.raw_text.startswith("ترجمه به انگلیسی : "):
                    text_wb = message.text.split(":")[-1]
                    response = get(f"https://api.codebazan.ir/translate/?type=json&from=fa&to=en&text={text_wb}")
                    data = json.loads(response.text)
                    text = data['result']
                    await message.reply(text)
                if message.raw_text and message.raw_text.startswith("اوقات شرعی : "):
                    text_wb = message.text.split(":")[-1]
                    string = ''
                    response = requests.get(f"https://api.codebazan.ir/owghat/?city={text_wb}")
                    if response.status_code == 200:
                        try:
                            response = response.json()
                            if response.get('Ok'):
                                results = response.get('Result')
                                for result in results:
                                    try:
                                        string += ''.join(['● شهر : ', result.get('shahr'), '\n', '● تاریخ : ', result.get('tarikh'),'\n', '● اذان صبج : ', result.get('azansobh'),'\n', '● طلوع صبح : ', result.get('toloaftab'),'\n', '● اذان ظهر : ', result.get('azanzohr'),'\n', '● غروب افتاب : ', result.get('ghorubaftab'),'\n', '● اذان مغرب : ', result.get('azanmaghreb'),'\n', '● نیمه شب : ', result.get('nimeshab')])
                                    except TypeError:
                                        continue
                                await message.reply(string)
                            else:
                                await message.reply("خطا در دریافت اطلاعات. لطفاً مجدداً تلاش کنید.")
                        except Exception as e:
                            traceback.print_exc()
                            await message.reply("خطای ناشناخته رخ داد.")
                    else:
                        await message.reply("خطا در دریافت اطلاعات. لطفاً مجدداً تلاش کنید.")
            if message.author_guid in admins and message.raw_text == "پاکسازی":
                await deleteMessages(client , message.message_id)
            
            if locks.locks["هوش مصنوعی"] == True:
                if message.raw_text and message.raw_text.startswith("//"):
                    text_wb = message.text.split("//")[-1]
                    response = requests.get(f"https://haji-api.ir/Free-GPT3/?text={text_wb}&key=hajiapi")
                    data = response.json()
                    message = data["result"]["message"]
                    await client.send_message(my_group,message,reply_to_message_id=msg)
            if locks.locks["حالت سخنگو"] == True:
                if message.raw_text not in commands_list:
                    text_wb = message.raw_text
                    response = requests.get(f"http://haji-api.ir/sokhan?text={text_wb}").text
                    await message.reply(response)

            if locks.locks["خوشامد گویی"] == True:
                result = await client.get_group_info(my_group)
                jd = result['group']['group_title']
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")
                current_date = datetime.date.today()
                formatted_dated = current_date.strftime("%Y-%m-%d")
                if message.raw_text == "یک عضو از طریق لینک به گروه افزوده شد.":
                    await message.delete_messages()
                    message_id = message.message_id
                    with open("wink-eye.mp4", "rb") as gif_file:
                        gif_data = gif_file.read()
                    resl = await client.send_gif(my_group, gif=gif_data, file_name="wink-eye.mp4" ,caption='✅یک کاربر در تاریخ:\n' + formatted_dated + '\n' + formatted_time + '\n به گروه  ' + jd + ' پیوست ✅\n @Id_Recod | کانال رسمی آرکد',reply_to_message_id=message_id)
                    jde = resl['message_update']['message_id']
                    await client.delete_messages(my_group,message_ids=jde)
                if message.raw_text == "یک عضو گروه را ترک کرد.":
                    await message.delete_messages()
                    reslg = await client.send_message(my_group,'❌یک کاربر در تاریخ:\n' + formatted_dated + '\n' + formatted_time + '\n از گروه  ' + jd + ' لفت داد ❌\n @Id_Recod | کانال رسمی آرکد',reply_to_message_id=msg)
                    jd = reslg['message_update']['message_id']
                    await client.delete_messages(my_group,message_ids=jd)
            result = message.to_dict().get("message")
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "Gif"
                    ):
                        await message.delete_messages()
                        print('Delete A Gif.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "Image"
                    ):
                        await message.delete_messages()
                        print('Delete A Image.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "Video"
                    ):
                        await message.delete_messages()
                        print('Delete A Video.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "Music"
                    ):
                        await message.delete_messages()
                        print('Delete A Music.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "Voice"
                    ):
                        await message.delete_messages()
                        print('Delete A Voice.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "File"
                    ):
                        await message.delete_messages()
                        print('Delete A File.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "poll"
                    ):
                        await message.delete_messages()
                        print('Delete A poll.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "location"
                    ):
                        await message.delete_messages()
                        print('Delete A location.')
            if locks.locks["عمل حذف گیف"] == False:
                if not message.author_guid in admins:
                    if (
                        "file_inline" in result
                        and result["file_inline"]["type"] == "live_data"
                    ):
                        await message.delete_messages()
                        print('Delete A live_data.')
            if locks.locks["حالت ضدلینک"] == False:
                raw_text = message.raw_text
                if not message.author_guid in admins:
                    if raw_text is not None and not raw_text in admins and ("https:" in raw_text or "@" in raw_text):
                        await message.delete_messages()
                        await client.ban_group_member(my_group,message.author_guid)
                        await client.send_message(my_group,"کاربر عزیز شما به علت اراسال لینک اخراج میشوید.",reply_to_message_id=msg)
                        print('Delete A Link.')
            if locks.locks["حالت فروارد"] == False:
                print("foll")
                if 'forwarded_from' in message.to_dict().get('message').keys():
                    await client.send_message(my_group,"کاربر عزیز شما به علت اراسال فروارد اخراج میشوید.",reply_to_message_id=msg)
                    await message.delete_messages()
                    print('Delete A forwarded.')
                    
        await client.run_until_disconnected()

run(main())
