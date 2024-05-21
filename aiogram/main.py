import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from api.api import *
from get_text.get_text import *
from buttons.buttons import *
from aiogram.fsm.context import FSMContext
from states.states import Form

TOKEN = "7161799077:AAGD0q6beFCeQWAsKJ280qaBxzuRxOvfwaM"
CHANEL = '-1002012167011'
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    user_exists = await create_user(user_id, username)
    lang = await get_user_language(user_id)
    if user_exists:
        await message.answer(await start_text(lang), parse_mode='markdown', reply_markup=await languages())
    else:
        await message.answer(await start_hello_text(lang), parse_mode='markdown', reply_markup=await languages())


@dp.message(lambda message: message.text == '🇺🇿 Uzbek' or message.text == '🇷🇺 Русский')
async def select_language(message: types.Message):
    user_id = message.from_user.id
    language = message.text
    text_language = await update_langugaes_text(language)
    await update_language_user(user_id, text_language)
    lang = await get_user_language(user_id)
    await message.answer(await start_text(lang), parse_mode='markdown', reply_markup=await main_menu(lang))


@dp.message(lambda message: message.text == "Katalog" or message.text == "Каталог")
async def catalog_menu(message: Message):
    user_id = message.from_user.id
    categories = await get_categories()
    check = await check_user_registration(user_id)
    lang = await get_user_language(user_id)
    text_1 = await get_registration_user(lang)
    text_2 = await get_not_registration_user(lang)
    if check is None:
        await message.answer(text_2, parse_mode='markdown', reply_markup=await user_registration(lang))
    else:
        await message.answer(text_1, parse_mode='markdown', reply_markup=await get_category(lang, categories))


@dp.message(lambda message: message.text in ['Ro\'yxatdan o\'tish', 'Зарегистрироваться'])
async def reaction_to_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    await message.answer(await state_user_name(lang), parse_mode='markdown', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.user_full_name)


@dp.message(Form.user_full_name)
async def process_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    if not (message.text.replace(' ', '').isalpha()) and len(message.text.split()) == 2:
        await message.answer(await state_error_username(lang), parse_mode='markdown')

    else:
        await state.update_data(user_full_name=message.text)
        await state.set_state(Form.phone_number)
        await message.answer(await get_user_phone(lang), parse_mode='markdown', reply_markup=await get_number(lang))
        await message.delete()


@dp.message(Form.phone_number)
async def get_user_phone_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_language(user_id)

    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
        data = await state.get_data()
        user_full_name = data.get('user_full_name', {})
        phone_number = data.get('phone_number', {})
        await insert_user_name_phone(user_id, user_full_name, phone_number)
        await state.clear()
        await message.answer(text=await success_registration(lang), parse_mode='markdown',
                             reply_markup=types.ReplyKeyboardRemove())
        await message.answer_photo(photo=types.FSInputFile('images/image.webp'), caption=await caption_company(lang),
                                   parse_mode="markdown", reply_markup=await main_menu(lang))
    else:
        await message.answer(await error_phone_user_number(lang))


@dp.callback_query(lambda call: 'category_id|' in call.data)
async def reaction_to_category(call: types.CallbackQuery):
    user_id = call.message.chat.id
    category_id = int(call.data.split('|')[1])
    lang = await get_user_language(user_id)
    await call.message.answer(text=await get_products_text(lang), parse_mode='markdown',
                              reply_markup=await get_product_by_pagination(category_id, lang))


@dp.callback_query(lambda call: 'next_category_page|' in call.data)
async def reaction_to_next_category(call: types.CallbackQuery):
    user_id = call.message.chat.id
    page = int(call.data.split("|")[1])
    lang = await get_user_language(user_id)
    new_page = page + 1

    category_data = await get_categories()
    inline_keyboard = await get_category(lang, category_data, new_page)
    await call.message.edit_reply_markup(reply_markup=inline_keyboard)


@dp.callback_query(lambda call: 'prev_category_page|' in call.data)
async def reaction_to_next_category(call: types.CallbackQuery):
    user_id = call.message.chat.id
    page = int(call.data.split("|")[1])
    lang = await get_user_language(user_id)
    new_page = max(1, page - 1)

    category_data = await get_categories()
    inline_keyboard = await get_category(lang, category_data, new_page)
    await call.message.edit_reply_markup(reply_markup=inline_keyboard)


@dp.callback_query(lambda call: "product_id|" in call.data)
async def reaction_to_product(call: types.CallbackQuery):
    user_id = call.message.chat.id
    lang = await get_user_language(user_id)
    product_id = int(call.data.split('|')[1])
    product = await get_product_detail(product_id)
    cat_id = product['category']
    product_name = product.get('product_name', {})
    product_price = product.get('product_price', {})
    product_image = product.get('product_image', {})
    text_products = await get_text_products_info(product_name, product_price, lang)
    if product_image is None:
        await call.message.answer_photo(photo=types.FSInputFile('image.jpg'), caption=text_products,
                                        parse_mode='markdown',
                                        reply_markup=await get_product_control_buttons(cat_id, product_id, 1, lang))

    else:
        await call.message.answer_photo(photo=product_image, caption=text_products, parse_mode='markdown',
                                        reply_markup=await get_product_control_buttons(cat_id, product_id, 1, lang))


@dp.callback_query(lambda call: call.data in ['minus', 'plus'])
async def reaction_plus_or_minus(call: types.CallbackQuery, bot: Bot):
    quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
    category_id = call.message.reply_markup.inline_keyboard[3][0].callback_data.split('|')[1]
    product_id = call.message.reply_markup.inline_keyboard[2][0].callback_data.split('|')[1]
    chat_id = call.message.chat.id
    lang = await get_user_language(chat_id)
    if call.data == 'plus':
        quantity += 1
    elif call.data == 'minus':
        if quantity > 1:
            quantity -= 1
    try:
        await bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                            reply_markup=await get_product_control_buttons(category_id, product_id,
                                                                                           quantity, lang))
    except Exception as e:
        pass


@dp.callback_query(lambda call: call.data.startswith('plus_'))
async def reaction_to_plus_increment(call: types.CallbackQuery, bot: Bot):
    increment_value = int(call.data.split('_')[1])
    category_id = call.message.reply_markup.inline_keyboard[3][0].callback_data.split('|')[1]
    product_id = call.message.reply_markup.inline_keyboard[2][0].callback_data.split('|')[1]
    chat_id = call.message.chat.id
    lang = await get_user_language(chat_id)

    quantity = int(call.message.reply_markup.inline_keyboard[0][1].text) + increment_value

    try:
        await bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                            reply_markup=await get_product_control_buttons(category_id, product_id,
                                                                                           quantity, lang))
    except Exception as e:
        pass


@dp.callback_query(lambda call: 'add|' in call.data)
async def process_add_button(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    product_id = int(call.data.split('|')[1])
    product = await get_product_detail(product_id)

    product_name, product_price = product['product_name'], product['product_price']
    quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)

    chat_id = call.message.chat.id
    lang = await get_user_language(chat_id)
    data = await state.get_data()
    card = data.get('cart', {})

    if product_name in card:
        card[product_name]['quantity'] += quantity
    else:
        card[product_name] = {
            'product_id': product_id,
            'price': product_price,
            'quantity': quantity
        }
    await state.set_data({'cart': card})
    await bot.answer_callback_query(call.id, text=await get_text_add_to_card(lang), show_alert=True)


@dp.callback_query(lambda call: 'show_card' in call.data)
async def show_cart_call_back(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cart = data.get('cart', {})

    chat_id = call.message.chat.id
    lang = await get_user_language(chat_id)

    if not cart:
        await call.answer(await get_not_cart(lang), show_alert=True)
    else:
        await call.message.answer(await get_info_cart_all(cart, lang), parse_mode='markdown',
                                  reply_markup=await show_card_buttons(cart, lang))


@dp.callback_query(lambda call: call.data.startswith('remove|'))
async def remove_product_from_cart(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    lang = await get_user_language(chat_id)
    product_id = int(call.data.split('|')[1])

    data = await state.get_data()
    card = data.get('cart', {})

    items_to_remove = []
    for product_name, product_values in card.items():
        if product_id == product_values['product_id']:
            items_to_remove.append(product_name)

    for item in items_to_remove:
        del card[item]

    await state.update_data(card=card)
    await call.message.answer(await get_info_cart_all(card, lang), parse_mode='markdown',
                              reply_markup=await show_card_buttons(card, lang))
    await call.message.delete()


@dp.callback_query(lambda call: call.data == "clear_data")
async def clear_cart_call_back(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = call.message.chat.id
    lang = await get_user_language(chat_id)

    data = await state.get_data()
    card = data.get('cart', {})

    card.clear()
    await state.update_data(card=card)
    await bot.delete_message(chat_id, call.message.message_id)
    await call.message.answer(await clear_data_cart(lang), reply_markup=await main_menu(lang), parse_mode='markdown')


@dp.callback_query(lambda call: call.data == 'submit')
async def submit_card(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = call.message.chat.id
    data = await state.get_data()
    user_info = await get_user_all_info(chat_id)
    lang = await get_user_language(chat_id)

    try:
        if chat_id == user_info.get('telegram_id', {}):
            user_name = user_info.get('user_full_name', None)
            user_phone = user_info.get('phone_number', None)
            user_tg_name = user_info.get('username', None)
            products = data.get('cart', {})

            for product_name, product_data in products.items():
                product_quantity = product_data.get('quantity', 0)
                product_price = product_data.get('price', 0)

                total_price = round(float(product_quantity) * float(product_price), 2)
                message_text = await get_card_text(user_name, user_tg_name, user_phone, product_name, product_quantity,
                                                   product_price, total_price)
                await bot.send_message(CHANEL, message_text)
                order_id = await create_orders(user_name, user_phone, user_tg_name)
                await create_orders_for_products({product_name: product_data}, order_id)
                await call.message.answer(f"Zakaz qabul qilindi")
                await call.message.delete()
    except Exception as e:
        pass


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
