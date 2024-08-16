from pyrogram import Client, filters
import os
import random

api_id = "25641220"  # Add your API ID
api_hash = "34f96c88a330d346e07f66d43af593c5"  # Add your API Hash
app = Client("my_account", api_id=api_id, api_hash=api_hash)

async def get_post(client, message):
    if "t.me" in message.text:
        parts = message.text.split("/")
        channel_username = parts[-2] if len(parts) > 2 else None
        post_id = int(parts[-1]) if len(parts) > 1 else None

        if channel_username and post_id:
            try:
                channel_info = await client.get_chat(channel_username)
                channel_id = channel_info.id

                msg = await client.get_messages(channel_id, post_id)
                await send_media_to_saved_messages(client, msg)
            except Exception as e:
                await client.send_message("me", f"Error in retrieving post: {str(e)}")
        else:
            await client.send_message("me", "Invalid post link.")
    else:
        await client.send_message("me", "Please provide a valid post link.")
import re

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

async def send_media_to_saved_messages(client, msg):
    try:
        media = None
        send_method = None
        file_path = None

        if msg.photo:
            file_name = "photo.png"
            file_path = await client.download_media(msg.photo, file_name=file_name)
            send_method = client.send_photo
        elif msg.video:
            file_name = "video.mp4"
            file_path = await client.download_media(msg.video, file_name=file_name)
            send_method = client.send_video
        elif msg.document:
            file_name = sanitize_filename(msg.document.file_name)
            file_path = await client.download_media(msg.document, file_name=file_name)
            send_method = client.send_document
        elif msg.audio:
            file_name = sanitize_filename(msg.audio.file_name)
            file_path = await client.download_media(msg.audio, file_name=file_name)
            send_method = client.send_audio
        elif msg.voice:
            file_name = "voice.ogg"
            file_path = await client.download_media(msg.voice, file_name=file_name)
            send_method = client.send_voice
        elif msg.animation:
            file_name = "animation.gif"
            file_path = await client.download_media(msg.animation, file_name=file_name)
            send_method = client.send_animation
        else:
            await client.send_message("me", "No supported media found in the specified post.")
            return

        if file_path and send_method:
            await send_method("me", file_path)
            await client.send_message("me", "File sent to Saved Messages.")

        if file_path:
            os.remove(file_path)

    except Exception as e:
        await client.send_message("me", f"Error in sending the file: {str(e)}")

async def reply_to_timed_media(client, message):
    try:
        if message.reply_to_message:
            media = None
            local = None
            caption = None

            if message.reply_to_message.photo:
                media = message.reply_to_message.photo
                rand = random.randint(1000, 9999999)
                local = f"downloads/photo-{rand}.png"
                caption = f"🔥 New timed image | Time: {media.ttl_seconds}s"
            elif message.reply_to_message.video:
                media = message.reply_to_message.video
                rand = random.randint(1000, 9999999)
                local = f"downloads/video-{rand}.mp4"
                caption = f"🔥 New timed video | Time: {media.ttl_seconds}s"

            if media and local:
                await client.download_media(message=message.reply_to_message, file_name=local)
                if message.reply_to_message.photo:
                    await client.send_photo("me", photo=local, caption=caption)
                elif message.reply_to_message.video:
                    await client.send_video("me", video=local, caption=caption)
                os.remove(local)
    except Exception as e:
        await client.send_message("me", f"Error downloading media: {e}")

@app.on_message(filters.me & filters.command("get_post", prefixes="/"))
async def handle_get_post(client, message):
    await get_post(client, message)

@app.on_message(filters.me & filters.reply & filters.text)
async def handle_reply_to_timed_media(client, message):
    await reply_to_timed_media(client, message)

def main():
    app.run()

if __name__ == "__main__":
    main()
