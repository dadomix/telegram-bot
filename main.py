import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your actual token
TOKEN = "7937749416:AAH5mabnGrLH-CfFZq4RSyoJTC49mDW3-fw"

# Enable logging to see actual errors in Railway logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 'style="success"' is supported in v21.1+ for the solid green look
    keyboard = [
        [InlineKeyboardButton("🛍 Shop", callback_data="shop")],
        [InlineKeyboardButton("« Back To Main Menu", callback_data="back", style="success")]
    ]
    await update.message.reply_text(
        "<b>⚜️ White X Modz Store ⚜️</b>\nSelect an option below:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "shop":
        keyboard = [[InlineKeyboardButton("« Back", callback_data="back", style="success")]]
        await query.edit_message_text("🏪 Select a Product", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "back":
        # Simplified back logic for testing
        pass

if __name__ == "__main__":
    # Modern setup for v20+ to avoid the 'Updater' AttributeError
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("Bot is starting on Railway with green button support...")
    app.run_polling()
