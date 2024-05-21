from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from api.api import get_products_by_category

BASE_URL = "http://127.0.0.1:8000/api/v1/categories/"


async def get_categories():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []


async def languages():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 Uzbek"),
            ],
            [
                KeyboardButton(text="🇷🇺 Русский"),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def main_menu(lang):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=lang == 'uz' and 'Katalog' or 'Каталог'),
                KeyboardButton(text=lang == 'uz' and 'Sozlamalar' or 'Настройки'),
            ],
            [
                KeyboardButton(text=lang == 'uz' and 'Biz bilan bog\'lanish' or 'Связаться с нами'),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def user_registration(lang):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=lang == 'uz' and "Ro'yxatdan o'tish" or "Зарегистрироваться"),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def get_number(lang):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=lang == 'uz' and "Raqamni yuborish" or "Отправить номер", request_contact=True),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def get_category(lang, categories, page=1, button_per_row=2):
    limit = 10
    offset = (page - 1) * limit
    counter = len(categories)
    max_page = counter // limit + (1 if counter % limit != 0 else 0)
    categories_to_show = categories[offset:offset + limit]
    button = []
    buttons = [
        InlineKeyboardButton(text=category['category_name'], callback_data=f"category_id|{category['id']}")
        for category in categories_to_show
    ]

    naxt_page_button_text, prev_page_button_text = '⏭', '⏮'

    pagination_buttons = [
        InlineKeyboardButton(text=prev_page_button_text, callback_data=f"prev_category_page|{page}"),
        InlineKeyboardButton(text=f"{page}", callback_data=f"current_page"),
        InlineKeyboardButton(text=naxt_page_button_text, callback_data=f"next_category_page|{page}")
    ]
    if page == 1:
        button += [InlineKeyboardButton(text=f"{page}", callback_data="current_page")]
        button += [InlineKeyboardButton(text=f"⏭", callback_data=f"next_page|{page}")]
    elif 1 < page < max_page:
        button += [InlineKeyboardButton(text=f'⏮', callback_data=f"previous|{page}")]
        button += [InlineKeyboardButton(text=f"{page}", callback_data="current_page")]
        button += [InlineKeyboardButton(text=f"⏭", callback_data=f"next_page|{page}")]
    elif page == max_page:
        button += [InlineKeyboardButton(text=f'⏮', callback_data=f"previous|{page}")]
        button += [InlineKeyboardButton(text=f"{page}", callback_data="current_page")]

    button_rows = [buttons[i:i + button_per_row] for i in range(0, len(buttons), button_per_row)]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[*button_rows, pagination_buttons])
    return inline_keyboard


async def get_product_by_pagination(category_id, lang, page=1, buttons_per_row=2):
    limit = 10
    offset = (page - 1) * limit
    products = await get_products_by_category(category_id)
    product = products.get('products', [])
    counter = len(product)

    max_page = counter // limit + (1 if counter % limit != 0 else 0)

    start_index = offset
    end_index = offset + limit

    buttons = [
        InlineKeyboardButton(text=produc['product_name'], callback_data=f"product_id|{produc['id']}")
        for produc in product[start_index:end_index]
    ]
    button = []
    button_row = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]

    if page > 1:
        button.append(InlineKeyboardButton(text="⏮", callback_data=f"previous_page|{category_id}"))

    button.append(InlineKeyboardButton(text=f"{page}", callback_data='current_page'))

    if page < max_page:
        button.append(InlineKeyboardButton(text='⏭', callback_data=f"next_page|{category_id}"))
    backs = [
        InlineKeyboardButton(text=lang == 'uz' and 'ortga' or 'назад', callback_data=f"category_backs"),
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[*button_row, button, backs])
    return inline_keyboard


async def get_product_control_buttons(category_id, product_id, quantity, lang):
    quantity_btn = [
        InlineKeyboardButton(text="➖", callback_data="minus"),
        InlineKeyboardButton(text=str(quantity), callback_data='quantity'),
        InlineKeyboardButton(text="➕", callback_data='plus')
    ]
    increment_btns = [
        InlineKeyboardButton(text="➕10", callback_data="plus_10"),
        InlineKeyboardButton(text='➕50', callback_data='plus_50'),
        InlineKeyboardButton(text="➕100", callback_data='plus_100')
    ]
    card = [
        InlineKeyboardButton(text=lang == 'uz' and "Savatga qoshish" or 'Добавить в корзину',
                             callback_data=f"add|{product_id}"),
        InlineKeyboardButton(text=lang == 'uz' and 'Savat' or "Корзина", callback_data=f"show_card")
    ]
    backs = [
        InlineKeyboardButton(text=lang == "uz" and "ortga" or "назад", callback_data=f"category_back|{category_id}")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[quantity_btn, increment_btns, card, backs])


async def show_card_buttons(data, lang):
    buttons = []
    if not data:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=lang == 'uz' and 'Savatingiz bo\'sh' or 'Ваша корзина пуста',
                                  callback_data="empty_cart")],
            [InlineKeyboardButton(text=lang == 'uz' and 'Katalog' or 'Каталог',
                                  callback_data="back_categories")]
        ])
    else:
        for product_name, items in data.items():
            product_id = items['product_id']
            button = InlineKeyboardButton(text=f"❌ {product_name}", callback_data=f"remove|{product_id}")
            buttons.insert(0, [button])
        markup = InlineKeyboardMarkup(inline_keyboard=[
            *buttons,
            [
                InlineKeyboardButton(text=lang == 'uz' and "Katalog" or "Каталог", callback_data="back_categories"),
                InlineKeyboardButton(text=lang == 'uz' and "Tozalash 🗑" or "Очистка 🗑", callback_data="clear_data"),
            ],
            [
                InlineKeyboardButton(text=lang == 'uz' and "Buyurtma berish ✅" or "заказать ✅", callback_data="submit"),
            ]
        ])
    return markup
