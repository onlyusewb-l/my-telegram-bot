import os
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# 🔑 NEW BOT TOKEN INTEGRATED
BOT_TOKEN = "8857558695:AAEIWWcuygCE2WnDrWaLoiS5eiDfb5pBADg"
bot = telebot.TeleBot(BOT_TOKEN)

# 📢 AAPKA CHANNEL USERNAME
CHANNEL_USERNAME = "@hardxxt"

# 🗂️ USER DATABASE (Plans aur Referrals tracking ke liye)
USER_PLANS = {}
USER_REF_COUNTS = {}  # Yahan har user ke refers save honge

# 📱 COMPLETE MIXED KEYBOARD (🔓 INSTAGRAM UNBAN removed)
def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🚫 INSTAGRAM ID BAN"),
        KeyboardButton("📸 CAMERA HACKER"),
        KeyboardButton("📞 CALL RECORDS HACK"),
        KeyboardButton("👤 BGMI PROFILE ANALYZER"),
        KeyboardButton("🎮 FREE FIRE PANEL"),
        KeyboardButton("🚀 FREE FOLLOWERS"),
        KeyboardButton("🌟 INSTAGRAM BLUE TICK"),
        KeyboardButton("🚙 VEHICLE LOOKUP"),
        KeyboardButton("⭐ Get Pro Access FREE!"),
        KeyboardButton("💬 DM FOR HELP"),
        KeyboardButton("📖 ALL TOOLS GUIDE"),
        KeyboardButton("💰 BUY PREMIUM")
    )
    return markup

# 💎 PREMIUM PLANS MENU
def premium_plans_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 ₹21 - Followers (10 Mins)", callback_data="p_21"),
        InlineKeyboardButton("💰 ₹99 - 7 Days Full", callback_data="p_99"),
        InlineKeyboardButton("💰 ₹149 - 15 Days Full", callback_data="p_149"),
        InlineKeyboardButton("💰 ₹249 - 1 Month Full", callback_data="p_249"),
        InlineKeyboardButton("💰 ₹449 - 2 Months Full", callback_data="p_449"),
        InlineKeyboardButton("💰 ₹599 - 3 Months Full", callback_data="p_599"),
        InlineKeyboardButton("💰 ₹999 - 6 Months Full", callback_data="p_999"),
        InlineKeyboardButton("💰 ₹1699 - 1 Year Full", callback_data="p_1699"),
        InlineKeyboardButton("❌ Cancel", callback_data="cancel_p")
    )
    return markup

# 🔒 INLINE CHANNEL LOCK KEYBOARD (INSTAGRAM ADDED)
def channel_lock_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 Updates ↗️", url="https://t.me/hardxxt"),
        InlineKeyboardButton("📺 YouTube Channel ↗️", url="https://youtube.com/@multixtgbot51"),
        InlineKeyboardButton("📸 Instagram ↗️", url="https://www.instagram.com/ayushnegyy_?igsh=eXJ4cHplMDIwMDRj"),
        InlineKeyboardButton("Joined ✅", callback_data="check_join")
    )
    return markup

# 🏁 START COMMAND (With Referral Link Detection)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1:
        try:
            inviter_id = int(args[1])
            if inviter_id != user_id:
                USER_REF_COUNTS[inviter_id] = USER_REF_COUNTS.get(inviter_id, 0) + 1
        except:
            pass

    must_join_text = (
        "♻️ Must Join Our All Channel\n\n"
        "♻️ After Joining Click On Joined"
    )
    bot.send_message(message.chat.id, must_join_text, parse_mode="Markdown", reply_markup=channel_lock_keyboard())

# 👑 ADMIN COMMAND TO ACTIVATE PLANS
@bot.message_handler(commands=['activate'])
def activate_user_plan(message):
    if message.from_user.username == "aayushnegi51":
        try:
            args = message.text.split()
            target_id = int(args[1])
            plan_type = args[2]
            
            USER_PLANS[target_id] = plan_type
            bot.reply_to(message, f"✅ User {target_id} ka plan successfully {plan_type.upper()} par activate kar diya gaya hai!")
            bot.send_message(target_id, f"🎉 Congratulations! Aapka Premium Plan ({plan_type.upper()}) activate ho gaya hai!")
        except:
            bot.reply_to(message, "❌ Format galat hai!")

# 🔄 CALLBACK HANDLER
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    
    if call.data == "check_join":
        try:
            member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
            joined = member.status in ['member', 'administrator', 'creator']
        except:
            joined = True

        if joined:
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            
            welcome_text = (
                f"⚠️ OWNER LIABILITY: The Owner (@aayushnegi51) is NOT responsible for any misuse, damage, or illegal activities caused by this bot.\n\n"
                f"👤 Aapki Telegram User ID: {user_id}"
            )
            bot.send_message(call.message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_keyboard())
        else:
            bot.answer_callback_query(call.id, "❌ Aapne abhi tak channel join nahi kiya hai!", show_alert=True)
            
    elif call.data == "cancel_p":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        
    elif call.data.startswith("p_"):
        price = call.data.split("_")[1]
        plan_names = {"21": "🚀 FREE FOLLOWERS PACK (10 MINS TRIAL)"}
        selected_plan = plan_names.get(price, "💎 FULL VIP ACCESS")
        
        pay_msg = (
            f"💳 SELECTED: {selected_plan}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💸 UPI PAYMENT DETAILS\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👉 Pay Amount: ₹{price}\n"
            f"📌 UPI ID: aayushnegi486@okaxis\n\n"
            f"⏱️ Validity: 10 Minutes Only!\n\n"
            f"ℹ️ Payment ke baad: Screenshot aur User ID ({user_id}) Admin ko bhejien.\n\n"
            "👑 Owner / Admin: @aayushnegi51"
        )
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa=aayushnegi486@okaxis%26am={price}%26cu=INR"
        bot.send_photo(call.message.chat.id, qr_url, caption=pay_msg, parse_mode="Markdown")

# 🎛️ SMART BUTTONS LOCK SYSTEM
@bot.message_handler(func=lambda message: message.text in [
    "🚫 INSTAGRAM ID BAN", "📸 CAMERA HACKER", "📞 CALL RECORDS HACK", 
    "👤 BGMI PROFILE ANALYZER", "🎮 FREE FIRE PANEL", "🚀 FREE FOLLOWERS", "🌟 INSTAGRAM BLUE TICK", 
    "🚙 VEHICLE LOOKUP", "📖 ALL TOOLS GUIDE", "💰 BUY PREMIUM", "💬 DM FOR HELP", "⭐ Get Pro Access FREE!"
])
def handle_hacking_buttons(message):
    btn = message.text
    user_id = message.from_user.id
    
    if btn == "💬 DM FOR HELP":
        bot.reply_to(message, "👑 Koi bhi problem ho to DM karein: https://t.me/aayushnegi51")
        return

    if btn == "⭐ Get Pro Access FREE!":
        pro_text = (
            "⭐ Get Pro Access FREE!\n\n"
            "1️⃣ Click the button below\n"
            "2️⃣ Watch a short ad\n"
            "3️⃣ Come back — Pro activates automatically!\n\n"
            "🎁 You'll get 3 days of Pro access"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔗 Watch Ad & Get Pro", url="https://shrinkme.click/LsvmQI"),
            InlineKeyboardButton("📩 Send Proof to Owner", url="https://t.me/aayushnegi51")
        )
        bot.send_message(message.chat.id, pro_text, reply_markup=markup)
        return

    user_access = USER_PLANS.get(user_id, "free")

    if btn == "💰 BUY PREMIUM":
        premium_text = "💎 SELECT YOUR PREMIUM PLAN\n\n👇 Choose a plan:"
        bot.send_message(message.chat.id, premium_text, parse_mode="Markdown", reply_markup=premium_plans_menu())
        return

    if btn == "📖 ALL TOOLS GUIDE":
        guide_text = (
            "⚙️ X MULTI TOOLS - COMPLETE USER GUIDE ⚙️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🚫 INSTAGRAM ID BAN: Simulation rules dashboard.\n"
            "📸 CAMERA HACKER: Dynamic sub-domain validation check.\n"
            "📞 CALL RECORDS HACK: Meta system logging trace.\n"
            "👤 BGMI PROFILE ANALYZER: Tier level and data status counter.\n"
            "🎮 FREE FIRE PANEL: Game settings layout optimization control.\n"
            "🚀 FREE FOLLOWERS: Real-time social metric simulator.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💎 *Saare tools ko chalane ke liye '💰 BUY PREMIUM' par click karke aaj hi VIP access unlock karein!*"
        )
        bot.send_message(message.chat.id, guide_text, parse_mode="Markdown")
        return

    has_access = False
    if user_access == "full":
        has_access = True
    else:
        if btn == "🚀 FREE FOLLOWERS" and user_access == "followers":
            has_access = True
        elif user_access == "free":
            has_access = False

    if has_access:
        bot.reply_to(message, f"✅ {btn} SIMULATION INTERFACE IS NOW RUNNING!\n\n👉 *Prank target details ya username format type karein...*")
    else:
        if btn == "🚀 FREE FOLLOWERS":
            required_plan = "💰 ₹21 - Followers Pack (10 Mins)"
        else:
            required_plan = "💎 FULL VIP SUBSCRIPTION (₹99+ Plans)"
            
        lock_text = (
            f"🔑 \"{btn}\" access blocked!\n\n"
            f"ℹ️ Is feature ko unlock karne ke liye aapke paas \"{required_plan}\" hona chahiye.\n\n"
            f"👉 Apni User ID ({user_id}) copy karein aur niche \"💰 BUY PREMIUM\" par click karke activate karein!"
        )
        bot.reply_to(message, lock_text)

# 📥 BACKGROUND LINKS DOWNLOADING
@bot.message_handler(func=lambda message: True)
def handle_all_other_inputs(message):
    inp = message.text.strip()
    if "instagram.com" in inp or "youtube.com" in inp or "youtu.be" in inp:
        sent_msg = bot.reply_to(message, "🔄 Processing your link... Please wait!")
        video_filename = f"dl_{message.chat.id}.mp4"
        ydl_opts = {'outtmpl': video_filename, 'format': 'best', 'quiet': True}
        try:
            with YoutubeDL(ydl_opts) as ydl: ydl.download([inp])
            if os.path.exists(video_filename):
                bot.edit_message_text("🚀 Uploading media to Telegram...", chat_id=message.chat.id, message_id=sent_msg.message_id)
                with open(video_filename, 'rb') as video:
                    bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
                os.remove(video_filename)
                bot.delete_message(chat_id=message.chat.id, message_id=sent_msg.message_id)
            else:
                bot.edit_message_text("❌ Download fail ho gaya.", chat_id=message.chat.id, message_id=sent_msg.message_id)
        except Exception:
            bot.edit_message_text("❌ Error processing media link!", chat_id=message.chat.id, message_id=sent_msg.message_id)
            if os.path.exists(video_filename): os.remove(video_filename)

print("X MULTI TOOLS Smart Billing System Online...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception:
        time.sleep(5)
          
