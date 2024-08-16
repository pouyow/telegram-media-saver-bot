# Telegram Media Saver Bot
#### Video Demo: [https://youtu.be/nsds6dGFsg4](https://youtu.be/nsds6dGFsg4)
#### Description:
This project is a Telegram bot that allows users to save media from posts in Telegram channels directly to their "Saved Messages." The bot can download and save photos, videos, documents, audio, and other types of media. Additionally, it can handle time-limited photos and automatically save them before they disappear.

## Features

- **Get and Save Media**: Retrieve media from a specified Telegram channel post and save it to your "Saved Messages."
- **Support for Multiple Media Types**: Handles photos, videos, documents, audio, voice messages, and animations.
- **Reply to Photo**: Automatically download and save time-limited photos from replies.
- **Error Handling**: Provides informative error messages if something goes wrong during media retrieval or saving.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/pouyow/telegram-media-saver-bot.git
    cd telegram-media-saver-bot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Telegram API credentials:
    - Obtain your `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).
    - Set these values in the `project.py` file.

## Usage

1. Start the bot by running:
    ```bash
    python project.py
    ```

2. In Telegram, send a command to the bot in the following format to save a post:
    ```
    /get_post https://t.me/channel/123
    ```
    - Replace `https://t.me/channel/123` with the actual link to the post you want to save.

3. To reply to a time-limited photo, reply with any text message to the photo, and the bot will automatically save it.

## Testing

To run the tests for this project:

```bash
pytest test_project.py
