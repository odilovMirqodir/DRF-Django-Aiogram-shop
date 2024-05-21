import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"


async def create_user(telegram_id, username):
    url = f"{BASE_URL}/users/"
    data = {
        "telegram_id": telegram_id,
        "username": username
    }
    headers = {
        'Content-Type': 'application/json'
    }

    check_user = f"{BASE_URL}/users/{telegram_id}/"
    check_user_response = requests.get(url=check_user)

    if check_user_response.status_code == 200:
        return True
    else:
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            print("foydalanuvchi yaratildi")
        else:
            print("Xatolik yuz berdi", response.status_code, response.text)


async def get_user_language(telegram_id):
    url = f"{BASE_URL}/users/{telegram_id}/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            user_data = response.json()
            language = user_data.get('language', {})
            if language:
                return language
            else:
                print("Language topilmadi")
        else:
            print(f"Response da xatolik {response.status_code},{response.text}")
    except Exception as e:
        print(f"Error: {e}")

    return None


async def update_language_user(user_id, language):
    url = f"{BASE_URL}/users/{user_id}/"
    data = {
        'language': language
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        check_user_response = requests.get(url=url)
        check_user_response.raise_for_status()

        if check_user_response.status_code == 200:
            response = requests.patch(url=url, data=json.dumps(data), headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                print(f"Foydalanuvchi tili yangilandi {language}")
            else:
                print(f"Xatolik yuz berdi:{response.status_code},{response.text}")
        else:
            print(f"Foydalanuvchi topilmadi")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


async def check_user_registration(user_id):
    url = f"{BASE_URL}/users/{user_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            user_data = response.json()
            phone_number, user_full_name = user_data.get('phone_number', {}), user_data.get('user_full_name', {})

            if phone_number and user_full_name is not None:
                return phone_number, user_full_name
            else:
                print(f"Foydalanuvchi raqami va username toplmadi")
        elif response.status_code == 404:
            print(f"User toplmadi")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


async def insert_user_name_phone(user_id, user_full_name, phone_number):
    url = f"{BASE_URL}/users/{user_id}/"
    data = {
        "user_full_name": user_full_name,
        "phone_number": phone_number
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        check_user_response = requests.get(url=url)
        check_user_response.raise_for_status()

        if check_user_response.status_code == 200:
            response = requests.patch(url=url, data=json.dumps(data), headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                print(f"Foydalanuvchi malumotlari yaxshi yangilandi")
            else:
                print(f"Malumotlarni yangilashta xatolik")
        else:
            print(f"Foydalanuvchi toplmadi")
    except requests.exceptions.RequestException as e:
        print(f"Request jonatishda xatolik: {e}")


async def get_products_by_category(category_id):
    url = f"{BASE_URL}/categories/{category_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            products = response.json()
            return products
        else:
            print(f"Product topilmadi")
    except requests.exceptions.RequestException as e:
        print(f"Error {e}")


async def get_product_detail(product_id):
    url = f"{BASE_URL}/products/{product_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Product topilmadi {response.status_code} {response.text}")
    except requests.RequestException as e:
        print(f"So'rov yuborishda xatolik yuz berdi {e}")


async def get_user_all_info(telegram_id):
    url = f"{BASE_URL}/users/{telegram_id}/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            print(f"{response.status_code} xatolik")
    except requests.RequestException as e:
        print(f"Soro'v yuborishda xatolik {e}")


async def create_orders(customer_name, customer_phone, customer_username):
    url = f"{BASE_URL}/orders/"
    data = {
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'customer_user_name': customer_username

    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        response.raise_for_status()

        order_id = response.json().get('id')
        print(f"Order yaratildi {order_id}")
        return order_id
    except requests.exceptions.HTTPError as error:
        print(f"HTTP ERROR {error}")
    except Exception as e:
        print(f"Error {e}")


async def create_orders_for_products(product_info, order_id):
    url = f"{BASE_URL}/order-items/"

    for product_name, product_data in product_info.items():
        product_quantity = product_data.get('quantity', 0)
        product_price = product_data.get('price', 0)
        total_price = round(float(product_quantity) * float(product_price), 2)

        data = {
            'product_name': product_name,
            'product_quantity': product_quantity,
            'product_price': product_price,
            'product_total_price': total_price,
            "order": order_id
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url=url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
            print(f"Product  {product_name} yaratildi")
        except requests.exceptions.HTTPError as error:
            print(f"HTTP ERROR {error}")
        except Exception as e:
            print(f"Error {e}")
