from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler
)
import os
import logging
from dotenv import load_dotenv

# ===================== ADMIN CONFIGURATION ZONE =====================
# Below are the settings you can adjust to customize the bot's behavior.

# List of user IDs to monitor. Only messages from these users will be filtered.
GRAY_LIST = [11111111111, 2222222222]

# Allowed words list. In ALLOWED_MODE, messages without any of these words will be deleted.
ALLOWED_WORDS = ["hello", "bye", "how", "are", "you"]

# Forbidden words list. In FORBIDDEN_MODE, messages containing any of these words will be deleted.
FORBIDDEN_WORDS = ["ad", "spam", "18+"]

# Enable or disable filtering modes:
# CHECK_ALLOWED: If True, delete messages that do NOT contain any word from ALLOWED_WORDS.
# CHECK_FORBIDDEN: If True, delete messages that contain at least one word from FORBIDDEN_WORDS.
# You can enable both modes at the same time if needed.
CHECK_ALLOWED = True      # Toggle Allowed-Words mode
CHECK_FORBIDDEN = True     # Toggle Forbidden-Words mode
# ===================================================================

# ===================== LOGGING CONFIGURATION =====================
# Configure logger to write violations to a file for later review.
# Suppress INFO logs from the Telegram internals to avoid polling noise,
# and record only violations at WARNING level.
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='violations.log',
    filemode='a',
    encoding='utf-8'
)
# Set Telegram library loggers to WARNING to disable polling logs
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('telegram.ext').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
# ===================================================================

async def filter_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for incoming messages. Applies filtering logic based on admin settings.
    Logs any deletions for review.
    """
    message = update.message
    if not message:
        return
    user = message.from_user
    user_id = user.id

    # Only process messages from users in the GRAY_LIST
    if user_id not in GRAY_LIST:
        return

    text = (message.text or "").strip()
    words = text.lower().split()

    # Prepare user identification for logs
    username = user.username or 'no_username'
    mention = f"@{username}" if user.username else user.first_name
    user_info = f"{user.full_name} ({user_id}, {mention})"

    # Allowed-Words mode: delete if no allowed words are present
    if CHECK_ALLOWED and not any(word in words for word in ALLOWED_WORDS):
        await message.delete()
        logger.warning(
            "Deleted message [no allowed words] from %s: '%s'",
            user_info,
            text
        )
        return

    # Forbidden-Words mode: delete if any forbidden word is present
    if CHECK_FORBIDDEN and any(word in words for word in FORBIDDEN_WORDS):
        await message.delete()
        logger.warning(
            "Deleted message [forbidden word] from %s: '%s'",
            user_info,
            text
        )
        return

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command handler. Confirms that the bot is online.
    """
    await update.message.reply_text("Anti-spam bot is online and ready to delete some spam!")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise RuntimeError("TOKEN is not set in .env")

    # Initialize the bot application with your token
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, filter_message)
    )

    # Start the bot in long-polling mode
    # allowed_updates specifies which types of updates to receive
    app.run_polling(
        allowed_updates=["message", "edited_channel_post", "edited_message"]
    )
