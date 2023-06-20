from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

order_button = ReplyKeyboardMarkup(resize_keyboard=True)
but_1 = KeyboardButton(text="/New_order")
but_2 = KeyboardButton(text="/End_day")
order_button.add(but_1).add(but_2)

new_day = ReplyKeyboardMarkup(resize_keyboard=True)
new_day_button = KeyboardButton(text="/New_day")
new_day.add(new_day_button)


cancel_button = ReplyKeyboardMarkup(resize_keyboard=True)
but_1 = KeyboardButton(text="/Cancel")
cancel_button.add(but_1)

check_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Yes", callback_data="yes")],
    [InlineKeyboardButton(text="No", callback_data='no')]
])

change_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Address", callback_data="ch_address"), InlineKeyboardButton(text="Phone number", callback_data="ch_phone")],
    [InlineKeyboardButton(text="Delivery time", callback_data='ch_del_time'), InlineKeyboardButton(text="Order", callback_data='ch_order')],
    [InlineKeyboardButton(text="Price", callback_data="ch_price")]
])

courier_inl_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Give to courier", callback_data="courier")],
    [InlineKeyboardButton(text="Cancel order", callback_data="ord_cancel")]
])


costemer_inl_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Delivered", callback_data="delivered")]
])