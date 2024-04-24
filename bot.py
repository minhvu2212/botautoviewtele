from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import requests
import asyncio
TELEGRAM_BOT_TOKEN = "xxxx"
API_TOKEN = "xxx"
HOST_URL = "https://apptanglike.com/api/v1"

def create_order(server_id, post_link, number_seeding):
    url = f"{HOST_URL}/order/create"
    headers = {"Accept": "application/json"}
    payload = {
        "api_token": API_TOKEN,
        "server_id": server_id,
        "post_link": post_link,
        "number_seeding": number_seeding,

    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Server 895: Tăng view telegram, min 100 1.5 đ", callback_data='895'), InlineKeyboardButton("Server 458: Tăng view telegram, min 100 1.5 đ", callback_data='458')],
        [InlineKeyboardButton("Server 846: Tăng view telegram, min 1k 1 đ", callback_data='846'), InlineKeyboardButton("Server 840: Tăng view telegram, min 100 1 đ", callback_data='840')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Vui lòng chọn server:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Bạn đã chọn server {query.data}. Vui lòng gửi link cần tăng view.")
    context.user_data['server_id'] = int(query.data)

def handle_link(update: Update, context: CallbackContext) -> None:
    server_id = context.user_data.get('server_id')
    post_link = update.message.text
    create_order(server_id, post_link, 200)
    update.message.reply_text("Đơn đặt hàng của bạn đã được tạo thành công!")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
