from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    user_full_name = State()
    phone_number = State()
    card = State()
    other_amount = State()
    custom_quantity = State()
