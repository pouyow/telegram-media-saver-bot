from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from project import get_post, send_media_to_saved_messages, reply_to_timed_media
import re
@pytest.mark.asyncio
async def test_get_post_valid_link():
    client = AsyncMock()
    message = MagicMock()
    message.text = "https://t.me/channelusername/123"

    channel_info_mock = MagicMock(id=123456)
    message_mock = MagicMock()

    client.get_chat = AsyncMock(return_value=channel_info_mock)
    client.get_messages = AsyncMock(return_value=message_mock)
    client.send_message = AsyncMock()

    with patch("project.send_media_to_saved_messages", new_callable=AsyncMock) as mock_send_media_to_saved_messages:
        await get_post(client, message)

        client.get_chat.assert_called_once_with("channelusername")
        client.get_messages.assert_called_once_with(123456, 123)
        mock_send_media_to_saved_messages.assert_called_once_with(client, message_mock)

@pytest.mark.asyncio
async def test_get_post_invalid_link():
    client = AsyncMock()
    message = MagicMock()
    message.text = "https://t.me/channelusername"

    client.send_message = AsyncMock()

    with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 10: 'channelusername'")):
        await get_post(client, message)
@pytest.mark.asyncio
async def test_send_media_to_saved_messages_photo():
    client = AsyncMock()
    msg = MagicMock()
    msg.photo = True
    client.download_media = AsyncMock(return_value="downloads_photo.png")
    client.send_photo = AsyncMock()

    with patch("os.remove") as mock_remove:
        await send_media_to_saved_messages(client, msg)

        client.download_media.assert_called_once_with(msg.photo, file_name="photo.png")
        client.send_photo.assert_called_once_with("me", "downloads_photo.png")
        mock_remove.assert_called_once_with("downloads_photo.png")

@pytest.mark.asyncio
async def test_reply_to_timed_media_photo():
    client = AsyncMock()
    media = MagicMock(ttl_seconds=10)
    message = MagicMock(reply_to_message=MagicMock(photo=media))

    client.download_media = AsyncMock(return_value="downloads/photo-1234567.png")
    client.send_photo = AsyncMock()

    with patch("random.randint", return_value=1234567):
        with patch("os.remove") as mock_remove:
            await reply_to_timed_media(client, message)

            client.download_media.assert_called_once_with(message=message.reply_to_message, file_name="downloads/photo-1234567.png")
            client.send_photo.assert_called_once_with("me", photo="downloads/photo-1234567.png", caption="🔥 New timed image | Time: 10s")
            mock_remove.assert_called_once_with("downloads/photo-1234567.png")
@pytest.mark.asyncio
async def test_reply_to_timed_media_video():
    client = AsyncMock()

    video_media = MagicMock(ttl_seconds=20)
    message = MagicMock(reply_to_message=MagicMock(video=video_media, photo=None))

    client.download_media = AsyncMock(return_value="downloads/video-7654321.mp4")
    client.send_video = AsyncMock()
    client.send_message = AsyncMock()

    with patch("random.randint", return_value=7654321):
        with patch("os.remove") as mock_remove:
            await reply_to_timed_media(client, message)

            client.download_media.assert_called_once_with(
                message=message.reply_to_message,
                file_name="downloads/video-7654321.mp4"
            )
            client.send_video.assert_called_once_with(
                "me",
                video="downloads/video-7654321.mp4",
                caption="🔥 New timed video | Time: 20s"
            )
            mock_remove.assert_called_once_with("downloads/video-7654321.mp4")

@pytest.mark.asyncio
async def test_get_post_no_link():
    client = AsyncMock()
    message = MagicMock()
    message.text = "Hello, this is a test message."

    client.send_message = AsyncMock()

    await get_post(client, message)

    client.send_message.assert_called_once_with("me", "Please provide a valid post link.")
