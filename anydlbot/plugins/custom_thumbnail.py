#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

import os
from PIL import Image
import time

from anydlbot import(
        AUTH_USERS,
        DOWNLOAD_LOCATION
)

# the Strings used for this "thing"
from translation import Translation

from pyrogram import(
        Client,
        Filters
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(Filters.photo)
async def save_photo(bot, update):
    if update.from_user.id not in AUTH_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION,
        "thumbnails"
    )
    thumb_image_path = os.path.join(
        thumbnail_location,
        str(update.from_user.id) + ".jpg"
    )
    if not os.path.isdir(thumbnail_location):
            os.makedirs(thumbnail_location)
    download_location = thumbnail_location + "/"
    downloaded_file_name = await bot.download_media(
        message=update,
        file_name=download_location
    )
    # https://stackoverflow.com/a/21669827/4723940
    Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
    metadata = extractMetadata(createParser(downloaded_file_name))
    height = 0
    if metadata.has("height"):
        height = metadata.get("height")
    # resize image
    # ref: https://t.me/PyrogramChat/44663
    img = Image.open(downloaded_file_name)
    # https://stackoverflow.com/a/37631799/4723940
    # img.thumbnail((320, 320))
     
    img.resize((320, height))
    img.save(thumb_image_path, "JPEG")
    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
    os.remove(downloaded_file_name)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
    # received single photo
    
    


@Client.on_message(Filters.command(["deletethumbnail"]))
async def delete_thumbnail(bot, update):
    if update.from_user.id not in AUTH_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    download_location = DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    try:
        os.remove(download_location + ".jpg")
        # os.remove(download_location + ".json")
        # os.remove(download_location + "usqp=CAU")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
