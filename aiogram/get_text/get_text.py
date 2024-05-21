async def start_text(language):
    if language == 'uz':
        return f"*Quyidagilardan birini tanlang*"
    else:
        return f"*Выберите один из следующих*"


async def start_hello_text(language):
    return f"*Assalomu aleykum Xush kelibsiz*" if language == 'uz' else f"*Привет и добро пожаловать*"


async def update_langugaes_text(language):
    return f"uz" if language == '🇺🇿 Uzbek' else f"ru"


async def get_registration_user(lang):
    return f"*Siz ro'yxatdan o'tkansiz ✅*" if lang == 'uz' else f"*Вы зарегистрированы ✅*"


async def get_not_registration_user(lang):
    if lang == 'uz':
        text = f"*Siz ro'yxatdan o'tmagansiz !\nIltimos Ro'yxatdan o'ting*"
    else:
        text = f"*Вы не зарегистрированы!\nПожалуйста, зарегистрируйтесь*"
    return text


async def state_user_name(lang):
    if lang == "uz":
        text = f"*Ism Familyangizni kiriting\nNamuna: Aziz Azizov*"
    else:
        text = f"*Введите свое имя и фамилию\nПример: Азиз Азизов*"
    return text


async def state_error_username(lang):
    if lang == "uz":
        text = f"*Iltimos Ism Familyangizni\nNamunadek kiriting*"
    else:
        text = f"*Пожалуйста, введите свое имя и фамилию в качестве примера.*"
    return text


async def get_user_phone(lang):
    if lang == "uz":
        text = f"*Raqamingiz yuboring*"
    else:
        text = f"*Отправьте свой номер*"
    return text


async def error_phone_user_number(lang):
    if lang == "uz":
        text = f"*Raqam yuborishta xatolik yuz berdi*"
    else:
        text = f"*Произошла ошибка при отправке номера*"
    return text


async def caption_company(lang):
    if lang == "uz":
        text = f"""*Engelbergdan bozorda energiya 
tejamkor plastik profil tizimlarining yangi avlodi. 
Issiqlik izolyatsiyasi va ovoz yalıtımı uchun yuqori talablarga ega xonalar uchun optimal variant. 
Biz bilan tanlash osonroq!*"""
    else:
        text = f"*Новое поколение энергоэффективных пластиковых профильных систем на рынке от Engelberg. Оптимальный вариант для помещений с высокими требованиями к теплоизоляции и шумоизоляции. С нами выбирать проще!*"
    return text


async def success_registration(lang):
    if lang == 'uz':
        text = f"*Ro'yxatdan o'tdingiz*"
    else:
        text = f"*Вы зарегистрировались*"
    return text


async def get_products_text(lang):
    return f"*Mahsulotlardan birini tanlang*" if lang == 'uz' else f"*Выберите один из продуктов*"


async def get_text_products_info(product_name, product_price, lang):
    if lang == 'uz':
        return f"*Mahsulot nomi: {product_name}\nMahsulot narxi: {product_price} usd*"
    else:
        return f"*Название продукта: {product_name}\nЦена продукта: {product_price} usd*"


async def get_text_add_to_card(lang):
    return f"Mahsulot savatga qoshildi" if lang == 'uz' else f"Продукт добавлен в корзину"


async def get_not_cart(lang):
    return f"Savatingiz bo'sh" if lang == 'uz' else f"Ваша корзина пуста"


async def get_info_cart_all(cart, lang):
    total_price = 0
    if lang == 'uz':
        if cart:
            cart_text = "Savatingizdagi Mahsulotlar:\n"

            for product_name, product_info in cart.items():
                product_price = product_info['price']
                product_quantity = product_info['quantity']
                product_total_price = round(float(product_quantity) * float(product_price), 2)
                cart_text += f"*Mahsulot nomi: {product_name}\n"
                cart_text += f"Mahsulot soni - {product_quantity} dona*\n"
                cart_text += f"Mahsulot narxi: {product_price} usd\n"
                total_price += product_total_price
            cart_text += f"Jami narxi: {total_price:.2f} usd"
        else:
            cart_text = "*Savatingiz bo'sh*"
    else:
        if cart:
            cart_text = "Товары в вашей корзине:\n"

            for product_name, product_info in cart.items():
                product_price = product_info['price']
                product_quantity = product_info['quantity']
                product_total_price = round(float(product_quantity) * float(product_price), 2)
                cart_text += f"*Наименование товара: {product_name}\n"
                cart_text += f"Номер продукта - {product_quantity} штук*\n"
                cart_text += f"Цена продукта: {product_price} usd\n"
                total_price += product_total_price
            cart_text += f"Общая стоимость: {total_price:.2f} usd"
        else:
            cart_text = "*Ваша корзина пуста*"
    return cart_text


async def clear_data_cart(lang):
    return f"*Savat tozalandi*" if lang == 'uz' else f"*Корзина очищена*"


async def get_card_text(user_name, user_tg_name, user_phone, product_name, product_quantity, product_price,
                        total_price):
    cart_text = f"Foydalanuvchi ismi: {user_name}\nFoydalanuvchi username: @{user_tg_name}\n"
    cart_text += f"Foydalanuvchi raqami: {user_phone}\n\nFoydalanuvchi Zakazi:\n\n"
    cart_text += f"Mahsulot nomi: {product_name}\nMahsulot soni: {product_quantity}"
    cart_text += f"Mahsulot narxi: {product_price}\nMahsulot summasi: {total_price}"
    return cart_text
