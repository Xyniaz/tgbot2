import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    LabeledPrice,
    PreCheckoutQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import Command
from aiosend import CryptoPay


BOT_TOKEN = "8071630752:AAFYVqOOJmZpL9etYmVa3vcxG6LnEvGr2G4"
CRYPTO_TOKEN = "538166:AA6OfYv9RNqgH5MAJ96ELr74KZEQ25k1NN8"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


cp = CryptoPay(CRYPTO_TOKEN)




@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Оплатить 2 USDT", callback_data="pay_crypto")
            ],
            [
                InlineKeyboardButton(text="⭐ Оплатить 200 Stars", callback_data="pay_stars")
            ]
        ]
    )

    await message.answer(
        "Для получения доступа к группе выберите способ оплаты:",
        reply_markup=keyboard
    )




@dp.callback_query(F.data == "pay_crypto")
async def crypto_callback(callback: CallbackQuery):
    await callback.answer()

    invoice = await cp.create_invoice(2, "USDT")
    await callback.message.answer(f"Оплатить: {invoice.bot_invoice_url}")

    invoice.poll(message=callback.message)


@cp.invoice_paid()
async def handle_crypto_payment(invoice, message: Message):
    await message.answer(
        f"✅ Платеж #{invoice.invoice_id} успешно оплачен!\n"
        "Вот ссылка на группу:\n"
        "https://t.me/+Uw3l9ySU-O42OTg5"
    )




@dp.callback_query(F.data == "pay_stars")
async def stars_callback(callback: CallbackQuery):
    await callback.answer()

    prices = [LabeledPrice(label="Доступ к группе", amount=200)]


    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Доступ к приватной группе",
        description="Оплата доступа через Telegram Stars",
        payload="stars-payment",
        provider_token="",  
        currency="XTR",     
        prices=prices,
    )



@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    await message.answer(
        "✅ Оплата прошла успешно!\n"
        "Вот ссылка на группу:\n"
        "https://t.me/+Uw3l9ySU-O42OTg5"
    )




async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        cp.start_polling(),
    )

if __name__ == "__main__":
    asyncio.run(main())
