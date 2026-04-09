import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging to see errors in Railway logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "7937749416:AAH5mabnGrLH-CfFZq4RSyoJTC49mDW3-fw"

def load_users():
    try:
        with open("users.json", "r") as f: return json.load(f)
    except: return {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    users = load_users()
    bal = users.get(uid, 0)
    
    text = f"⚜️ White X Modz Store ⚜️\n━━━━━━━━━━━━━━━━━━\n💰 Balance: ₹{bal}\n━━━━━━━━━━━━━━━━━━"
    keyboard = [
        [InlineKeyboardButton("🛍 Shop", callback_data="shop")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "shop":
        keyboard = [
            [InlineKeyboardButton("🔥 Drip Client", callback_data="drip")],
            # THIS IS THE GREEN BUTTON THAT WAS CRASHING
            [InlineKeyboardButton("« Back To Main Menu", callback_data="back_main", style="success")]
        ]
        await query.edit_message_text("🏪 Select Product:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data == "back_main":
        uid = str(update.effective_user.id)
        users = load_users()
        bal = users.get(uid, 0)
        text = f"⚜️ White X Modz Store ⚜️\n━━━━━━━━━━━━━━━━━━\n💰 Balance: ₹{bal}\n━━━━━━━━━━━━━━━━━━"
        keyboard = [
            [InlineKeyboardButton("🛍 Shop", callback_data="shop")],
            [InlineKeyboardButton("👤 Profile", callback_data="profile")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == "__main__":
    # The modern ApplicationBuilder for v20+
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("Bot is starting...")
    app.run_polling()
