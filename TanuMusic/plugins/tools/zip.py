import os
import zipfile

from pyrogram import filters
from TanuMusic import app


def zip_file(file_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w") as zf:
        zf.write(file_path, os.path.basename(file_path))


def unzip_file(zip_file_path, output_folder):
    with zipfile.ZipFile(zip_file_path, "r") as zf:
        zf.extractall(output_folder)


@app.on_message(filters.command("zip"))
async def zip_command(client, message):
    if message.reply_to_message and message.reply_to_message.document:
        original_file = await client.download_media(message.reply_to_message)
        zip_file_path = f"{original_file}.zip"
        zip_file(original_file, zip_file_path)
        await message.reply_document(zip_file_path)
        try:
            os.remove(zip_file_path)
            os.remove(original_file)
        except Exception:
            pass
    else:
        await message.reply_text("Reply to a file with /zip")


@app.on_message(filters.command("unzip"))
async def unzip_command(client, message):
    if (
        message.reply_to_message
        and message.reply_to_message.document
        and message.reply_to_message.document.file_name.endswith(".zip")
    ):
        zip_file_path = await client.download_media(message.reply_to_message)
        output_folder = f"{zip_file_path}_unzipped"
        os.makedirs(output_folder, exist_ok=True)
        unzip_file(zip_file_path, output_folder)
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                await message.reply_document(os.path.join(root, file))
    else:
        await message.reply_text("Reply to a .zip with /unzip")
