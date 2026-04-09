import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = "7937749416:AAH5mabnGrLH-CfFZq4RSyoJTC49mDW3-fw"
ADMIN_ID = 8343432155

# --- DATA STORAGE ---
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

# --- PRICES ---
prices = {
    "dripnr": {"1": 79, "3": 177, "7": 349, "15": 589, "30": 889},
    "dripr": {"1": 79, "7": 319, "30": 829},
    "hg": {"1": 95, "2": 159, "10": 288, "30": 649},
    "patonr": {"3": 210, "7": 329, "15": 612, "30": 998},
    "prime": {"1": 69, "5": 169, "10": 329},
}

# --- MENU HELPERS ---
def get_main_keyboard(uid):
    users = load_users()
    bal = users.get(str(uid), 0)
    text = (f"⚜️ White X Modz Store ⚜️\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💰 Balance: ₹{bal}\n"
            f"━━━━━━━━━━━━━━━━━━")
    keyboard = [
        [InlineKeyboardButton("🛍 Shop", callback_data="shop")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("💰 Add Balance", callback_data="addbalance")]
    ]
    return text, InlineKeyboardMarkup(keyboard)

# --- COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text, markup = get_main_keyboard(uid)
    await update.message.reply_text(text, reply_markup=markup)

async def addcredit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        user_id = context.args[0]
        amount = float(context.args[1])
        users = load_users()
        users[user_id] = users.get(user_id, 0) + amount
        save_users(users)
        await update.message.reply_text(f"✅ Added ₹{amount} to {user_id}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /addcredit ID AMOUNT")

# --- CALLBACK HANDLER (The Green Buttons) ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    data = query.data

    if data == "back_main":
        text, markup = get_main_keyboard(uid)
        await query.edit_message_text(text, reply_markup=markup)

    elif data == "shop":
        text = "🏪 SELECT CATEGORY"
        keyboard = [
            [InlineKeyboardButton("🔥 Drip (Non-Root)", callback_data="panel_dripnr")],
            [InlineKeyboardButton("🔥 Drip (Root)", callback_data="panel_dripr")],
            # THIS IS THE GREEN BUTTON
            [InlineKeyboardButton("« Back To Main Menu", callback_data="back_main", style="success")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("panel_"):
        panel = data.split("_")[1]
        text = f"🛒 {panel.upper()} PACKAGES"
        keyboard = []
        for days, price in prices.get(panel, {}).items():
            keyboard.append([InlineKeyboardButton(f"🛒 {days} Day - ₹{price}", callback_data=f"buy_{panel}_{days}")])
        
        # ANOTHER GREEN BUTTON
        keyboard.append([InlineKeyboardButton("« Back To Shop", callback_data="shop", style="success")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# --- MAIN BOOTLOGIC ---
if __name__ == "__main__":
    # ApplicationBuilder is the modern way to start bots in v20+
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addcredit", addcredit))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Bot is running on Railway with Green Button Support!")
    app.run_polling()
