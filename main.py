from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import json
import storage

TOKEN = "7937749416:AAH5mabnGrLH-CfFZq4RSyoJTC49mDW3-fw"
ADMIN_ID = 8343432155
ADMIN_USERNAME = "DADFROZ_GAMERZ"

prices = {
    "dripnr": {"1": 79, "3": 129, "7": 319, "15": 549, "30": 829},
    "dripr": {"1": 79, "7": 319, "30": 829},
    "hg": {"1": 95, "2": 159, "10": 288, "30": 649},
    "patonr": {"3": 210, "7": 329, "15": 612, "30": 998},
    "prime": {"1": 69, "5": 169, "10": 329},
    "reaperr": {"10": 338, "30": 848},
    "haxx": {"10": 499},
    "br": {"1": 75, "7": 239, "15": 389, "30": 521},
    "fluorite": {"1": 429, "7": 1198, "30": 2199},
    "streamer": {"10": 400, "20": 800, "30": 1100},
    "alphahaxx": {
        "1h": 8,
        "2h": 25,
        "5h": 50,
        "7": 320,
        "14": 560,
        "30": 720
    },
}

upgrade_prices = {
    "dripnr": {"1": 50, "3": 90, "7": 200, "15": 350, "30": 550},
    "dripr": {"1": 50, "7": 200, "30": 550},
    "hg": {"1": 60, "2": 100, "10": 180, "30": 420},
    "patonr": {"3": 140, "7": 220, "15": 400, "30": 650},
    "prime": {"1": 45, "5": 110, "10": 210},
    "reaperr": {"10": 220, "30": 550},
    "haxx": {"10": 320},
    "br": {"1": 50, "7": 160, "15": 250, "30": 340},
    "fluorite": {"1": 280, "7": 780, "30": 1450},
    "streamer": {"10": 260, "20": 520, "30": 720},
    "alphahaxx": {"1h": 5, "2h": 16, "5h": 32, "7": 210, "14": 365, "30": 470},
}

# ---------- UPGRADED USERS ----------

def load_upgraded():
    try:
        with open("upgraded.json", "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_upgraded(data):
    with open("upgraded.json", "w") as f:
        json.dump(list(data), f)

def get_price(uid, panel, days):
    upgraded = load_upgraded()
    if uid in upgraded and panel in upgrade_prices and days in upgrade_prices[panel]:
        return upgrade_prices[panel][days]
    return prices[panel][days]

# ---------- USERS ----------

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- HISTORY ----------

def load_history():
    try:
        with open("history.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_history(data):
    with open("history.json", "w") as f:
        json.dump(data, f, indent=4)

# ---------- MAIN MENU ----------

def main_menu(uid):
    users = load_users()
    bal = users.get(uid, 0)

    upgraded = load_upgraded()
    upgrade_tag = " ⭐ UPGRADED" if uid in upgraded else ""

    text = (
        "⚜️ FUCK GENERATOR ⚜️\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"💰 Rupees: ₹{bal}{upgrade_tag}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔥 Premium Panels Available\n"
        "🔥 Instant Delivery\n"
        "🔥 Add Balance to Purchase\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📞 Contact : @DADFROZ_GAMERZ"
    )

    keyboard = [
        [InlineKeyboardButton("🛍 Shop", callback_data="shop")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("💰 Add Balance", callback_data="addbalance")],
        [InlineKeyboardButton("📄 History", callback_data="history_user")]
    ]

    return text, keyboard

# ---------- START ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.message.from_user.id)
    text, keyboard = main_menu(uid)
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---------- ADMIN HISTORY ----------

async def history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Not allowed")
        return

    users = load_users()
    if not users:
        await update.message.reply_text("No users found")
        return

    keyboard = []

    for uid in users.keys():
        try:
            chat = await context.bot.get_chat(int(uid))
            name = chat.first_name or "User"
        except:
            name = "Unknown"

        keyboard.append([
            InlineKeyboardButton(f"👤 {name} ({uid})", callback_data=f"admin_user_{uid}")
        ])

    keyboard.append([InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="back_main", style="success")])

    await update.message.reply_text(
        "📄 Select a user:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- BROADCAST ----------

async def sendmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: /sendmessage text")
        return

    message = " ".join(context.args)
    users = load_users()

    success, failed = 0, 0

    for uid in users.keys():
        try:
            await context.bot.send_message(chat_id=int(uid), text=message)
            success += 1
        except:
            failed += 1

    await update.message.reply_text(f"✅ Sent: {success}\n❌ Failed: {failed}")

# ---------- STOCK ----------

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        with open("keys.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    text = "📦 STOCK\n\n"

    for panel in prices:
        text += f"🔹 {panel.upper()}\n"

        for days in prices[panel]:
            keys_list = []

            if panel in data and isinstance(data[panel], dict):
                keys_list = data[panel].get(days, [])

            count = len(keys_list) if isinstance(keys_list, list) else 0

            label = f"{days.replace('h','')} Hour" if "h" in days else f"{days} Days"
            text += f"    {label} → {count} keys\n"

        text += "\n"

    await update.message.reply_text(text)

# ---------- UPGRADE ----------

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /upgrade USER_ID")
        return

    target_uid = context.args[0]
    upgraded = load_upgraded()
    upgraded.add(target_uid)
    save_upgraded(upgraded)

    await update.message.reply_text(f"✅ User {target_uid} has been upgraded to discounted prices!")

async def downgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /downgrade USER_ID")
        return

    target_uid = context.args[0]
    upgraded = load_upgraded()
    upgraded.discard(target_uid)
    save_upgraded(upgraded)

    await update.message.reply_text(f"✅ User {target_uid} has been removed from upgraded users.")

# ---------- CALLBACK ----------

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    uid = str(query.from_user.id)

    if data.startswith("admin_user_"):
        target_uid = data.split("_")[2]
        history = load_history()
        users = load_users()

        balance = users.get(target_uid, 0)

        upgraded = load_upgraded()
        upgrade_status = "⭐ Upgraded" if target_uid in upgraded else "Regular"

        text = f"👤 User ID: {target_uid}\n💰 Rupees: {balance}\n🏷 Status: {upgrade_status}\n\n📄 History:\n\n"

        if target_uid in history:
            for item in history[target_uid]:
                text += f"{item['panel']} | {item['days']}\n{item['key']}\n\n"
        else:
            text += "No history"

        keyboard = [[InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="back_main", style="success")]]

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "back_main":
        text, keyboard = main_menu(uid)
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "shop":
        upgraded = load_upgraded()
        upgrade_tag = " ⭐ UPGRADED PRICES" if uid in upgraded else ""

        text = (
            f"🏪 LICENSE KEY GENERATOR STORE 🏪\n\n"
            f"⚜️ License Key Generator\n"
            f"⚜️ Instant Delivery\n"
            f"⚜️ Secure Payment\n"
            f"⚜️ Premium Keys\n"
            f"📞 24/7 Support\n\n"
            f"👇 Please Select Your Product 👇\n\n"
            f"💰 Rupees: ₹{load_users().get(uid, 0)}{upgrade_tag}"
        )

        keyboard = [
            [InlineKeyboardButton("🔥 Drip Client (Non Root)", callback_data="panel_dripnr")],
            [InlineKeyboardButton("🔥 Drip Client (Root)", callback_data="panel_dripr")],
            [InlineKeyboardButton("⚡ HG Mod (Non-Root+Root)", callback_data="panel_hg")],
            [InlineKeyboardButton("🦆 Pato Team (Non Root)", callback_data="panel_patonr")],
            [InlineKeyboardButton("🪝 Prime Hook (Non-Root)", callback_data="panel_prime")],
            [InlineKeyboardButton("☠️ Reaper X Pro (Root)", callback_data="panel_reaperr")],
            [InlineKeyboardButton("♋ Haxx-cker Pro (Root)", callback_data="panel_haxx")],
            [InlineKeyboardButton("🌀 BR Mod (Root)", callback_data="panel_br")],
            [InlineKeyboardButton("🍎 Fluorite (iOS)", callback_data="panel_fluorite")],
            [InlineKeyboardButton("👁️ Streamer X Shadow", callback_data="panel_streamer")],
            [InlineKeyboardButton("❤️‍🔥 ALPHA HAXX", callback_data="panel_alphahaxx")],
            [InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="back_main", style="success")]
        ]

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("panel_"):
        panel = data.split("_")[1]

        try:
            with open("keys.json", "r") as f:
                stock_data = json.load(f)
        except:
            stock_data = {}

        panel_names = {
            "dripnr": "DRIP CLIENT - NON ROOT",
            "dripr": "DRIP CLIENT - ROOT",
            "hg": "HG MOD (NON-ROOT+ROOT)",
            "patonr": "PATO TEAM (NON ROOT)",
            "prime": "PRIME HOOK (NON-ROOT)",
            "reaperr": "REAPER X PRO (ROOT)",
            "haxx": "HAXX-CKER PRO (ROOT)",
            "br": "BR MOD (ROOT)",
            "fluorite": "FLUORITE (IOS)",
            "streamer": "STREAMER X SHADOW",
            "alphahaxx": "ALPHA HAXX"
        }
        panel_title = panel_names.get(panel, panel.upper())

        text = f"🛒 {panel_title}\n━━━━━━━━━━━━━━━━━━\n\n📦 Package Info:\n"
        keyboard = []

        keys_list = list(prices[panel].keys())
        for i, days in enumerate(keys_list):
            price = get_price(uid, panel, days)
            label_upper = f"{days.replace('h','')} HOUR" if "h" in days else f"{days} DAY"
            label_btn = f"{days.replace('h','')} Hour" if "h" in days else f"{days} Day"

            keys_avail = []
            if panel in stock_data and isinstance(stock_data[panel], dict):
                keys_avail = stock_data[panel].get(days, [])

            count = len(keys_avail) if isinstance(keys_avail, list) else 0

            stock_status = "✅ Stock Available" if count > 0 else "❌ Out of Stock"
            prefix = "└" if i == len(keys_list) - 1 else "├"

            text += f"{prefix} {label_upper} : ₹{price} - {count} stock\n{stock_status}\n\n"

            keyboard.append([
                InlineKeyboardButton(f"🛒 {label_btn} - ₹{price}", callback_data=f"buy_{panel}_{days}"),
                InlineKeyboardButton("📦 Bulk", callback_data=f"bulk_{panel}_{days}")
            ])

        text += "Prices are auto-calculated based on your tier."

        # BACK BUTTON TO GREEN
        keyboard.append([InlineKeyboardButton("« Back To Store", callback_data="shop", style="success")])

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("bulk_"):
        _, panel, days = data.split("_")

        context.user_data["bulk_panel"] = panel
        context.user_data["bulk_days"] = days
        context.user_data["awaiting_bulk"] = True

        await query.edit_message_text(
            f"📦 Enter quantity for {panel.upper()} ({days}):\n\nSend like:\n10"
        )

    elif data.startswith("buy_"):
        _, panel, days = data.split("_")

        price = get_price(uid, panel, days)
        label = f"{days.replace('h','')} Hour" if "h" in days else f"{days} Days"

        keyboard = [
            [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{panel}_{days}")],
            [InlineKeyboardButton("❌ Cancel", callback_data=f"panel_{panel}")]
        ]

        await query.edit_message_text(
            f"⚠️ CONFIRM PURCHASE\n\n{panel.upper()} | {label}\n💰 Price: ₹{price} Rupees\n\nAre you sure?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "confirm_bulk":
        uid = str(query.from_user.id)

        panel = context.user_data.get("bulk_panel")
        days = context.user_data.get("bulk_days")
        qty = context.user_data.get("bulk_qty")

        users = load_users()
        balance = users.get(uid, 0)
        price = get_price(uid, panel, days)
        total = price * qty

        if balance < total:
            await query.answer("❌ Not enough credits!", show_alert=True)
            return

        keys = []

        for _ in range(qty):
            key = storage.get_key(panel, days)
            if not key:
                break
            keys.append(key)

        if not keys:
            await query.edit_message_text("❌ OUT OF STOCK")
            return

        users[uid] -= price * len(keys)
        save_users(users)

        history = load_history()
        history.setdefault(uid, [])

        for key in keys:
            history[uid].append({
                "panel": panel,
                "days": days,
                "key": key
            })

        save_history(history)

        keys_text = "\n".join(keys)

        keyboard = [[InlineKeyboardButton("⬅️ Back To Shop", callback_data="shop", style="success")]]

        await query.edit_message_text(
            f"✅ BULK PURCHASE SUCCESS\n\n"
            f"{panel.upper()} | {days}\n"
            f"Qty: {len(keys)}\n\n🔑 Keys:\n{keys_text}\n\n"
            f"💰 Remaining: ₹{users[uid]}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("confirm_"):
        _, panel, days = data.split("_")

        users = load_users()
        balance = users.get(uid, 0)
        price = get_price(uid, panel, days)

        if balance < price:
            await query.answer("❌ Not enough credits!", show_alert=True)
            return

        key = storage.get_key(panel, days)

        if not key:
            keyboard = [[InlineKeyboardButton("⬅️ Back To Panel", callback_data=f"panel_{panel}", style="success")]]
            await query.edit_message_text("❌ OUT OF STOCK", reply_markup=InlineKeyboardMarkup(keyboard))
            return

        users[uid] -= price
        save_users(users)

        history = load_history()
        history.setdefault(uid, []).append({
            "panel": panel,
            "days": days,
            "key": key
        })
        save_history(history)

        label = f"{days.replace('h','')} Hour" if "h" in days else f"{days} Days"

        keyboard = [[InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="shop", style="success")]]

        await query.edit_message_text(
            f"✅ PURCHASE SUCCESS\n\n{panel.upper()} | {label}\n\n🔑 {key}\n\n💰 Remaining: ₹{users[uid]}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "profile":
        bal = load_users().get(uid, 0)
        upgraded = load_upgraded()
        status = "⭐ Upgraded" if uid in upgraded else "Regular"
        text = f"👤 Profile\n\nID: {uid}\nRupees: ₹{bal}\nStatus: {status}"
        keyboard = [[InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="back_main", style="success")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "addbalance":
        text = "💰 Add Balance\n\nContact Admin\n@DADFROZ_GAMERZ"
        keyboard = [
            [InlineKeyboardButton("📩 Contact Admin", url="https://t.me/DADFROZ_GAMERZ")],
            [InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="back_main", style="success")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "history_user":
        hist = load_history()
        text = "📄 Your History\n\n"

        if uid in hist:
            for item in hist[uid]:
                text += f"{item['panel']} | {item['days']}\n{item['key']}\n\n"
        else:
            text += "No history"

        keyboard = [[InlineKeyboardButton("⬅️ Back To Main Menu", callback_data="back_main", style="success")]]

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---------- BULK INPUT ----------

async def bulk_quantity_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_bulk"):
        return

    uid = str(update.message.from_user.id)

    try:
        qty = int(update.message.text.strip())
        if qty <= 0:
            raise ValueError
    except:
        await update.message.reply_text("❌ Invalid quantity")
        return

    panel = context.user_data["bulk_panel"]
    days = context.user_data["bulk_days"]

    price = get_price(uid, panel, days)
    total = price * qty

    context.user_data["bulk_qty"] = qty
    context.user_data["awaiting_bulk"] = False

    keyboard = [
        [InlineKeyboardButton("✅ Confirm Bulk", callback_data="confirm_bulk")],
        [InlineKeyboardButton("❌ Cancel", callback_data=f"panel_{panel}")]
    ]

    await update.message.reply_text(
        f"⚠️ BULK PURCHASE\n\n{panel.upper()} | {days}\nQty: {qty}\n💰 Total: ₹{total}\n\nConfirm?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- ADMIN ----------

async def addcredit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addcredit USER_ID AMOUNT")
        return

    uid = context.args[0]

    try:
        amount = float(context.args[1])
    except:
        await update.message.reply_text("Invalid amount")
        return

    users = load_users()
    users[uid] = users.get(uid, 0) + amount
    save_users(users)

    await update.message.reply_text("Done")

async def addkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/addkey panel days\nkey1\nkey2\nkey3..."
        )
        return

    panel = context.args[0]
    days = context.args[1]

    lines = update.message.text.split("\n")
    keys = lines[1:]

    added = 0

    for key in keys:
        key = key.strip()
        if key:
            storage.add_key(panel, days, key)
            added += 1

    await update.message.reply_text(f"✅ Added {added} keys successfully!")

# ---------- RUN ----------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addcredit", addcredit))
app.add_handler(CommandHandler("addkey", addkey))
app.add_handler(CommandHandler("history", history_cmd))
app.add_handler(CommandHandler("sendmessage", sendmessage))
app.add_handler(CommandHandler("stock", stock))
app.add_handler(CommandHandler("upgrade", upgrade))
app.add_handler(CommandHandler("downgrade", downgrade))
app.add_handler(CallbackQueryHandler(callback_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bulk_quantity_handler))

app.run_polling()