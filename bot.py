from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio import sleep
from config import TOKEN, group_id # Bot tokken and group id 
from buttons import order_button, cancel_button, check_keyboard, change_keyboard, courier_inl_kb, costemer_inl_kb, new_day
from datetime import datetime


bot = Bot(TOKEN) #Your bot token here
storage = MemoryStorage()
dp = Dispatcher(bot,
                storage=storage)

async def on_startup(_):
    print("Bot is online")

#________________Bot FSM States don't touch it__________
class OrderStatesGroup(StatesGroup):
    address = State()
    phone = State()
    del_time = State()
    order = State()
    price = State()
    chack = State()
    problem = State()
    change_address = State()
    change_phone = State()
    change_del_time = State()
    change_order = State()
    change_price = State()



@dp.message_handler(commands=["Start"])
async def cmd_start(msg:types.Message) -> None:
    global kassa
    global delivery_count
    kassa = 0
    delivery_count = 0
    await msg.answer(text=f"Welcome {msg.from_user.first_name}", reply_markup=order_button)

@dp.message_handler(commands=["help"])
async def cmd_help(msg:types.Message) -> None:
    await msg.answer(text = """Hello I am delivery bot\nPress New_order button and go step by step to create a order\n
    After that i will send your order to delivery group\n
    In delivery group thete is 2 buttons and easy to understand\n
    press End_day and you will get deliveries cound, and sum of all deliveries\n
    press New_day to start new day""")
    
#_____________________Order Block__________________________

@dp.message_handler(commands=["Cancel"], state="*")
async def cmd_cancel(msg:types.Message, state:FSMContext) -> None:
    if state is None:
        return
    await state.finish()
    await msg.answer("Order cancelled", reply_markup=order_button)


@dp.message_handler(commands=["New_order"])
async def cmd_order(msg:types.Message) -> None:
    await msg.answer(text="Creating new order!\nPlease write delivery address", reply_markup=cancel_button)
    await OrderStatesGroup.address.set()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.address)
async def load_address(msg:types.Message, state:FSMContext) -> None:
    async with state.proxy() as data:
        data["address"] = msg.text
    await msg.answer(text="Ok. Now write please customer phone number")
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.phone)
async def load_phone(msg:types.Message, state:FSMContext) -> None:
    async with state.proxy() as data:
        data["phone"] = msg.text
    await msg.answer(text="Good! Now write please delivery time")
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.del_time)
async def load_del_time(msg:types.Message, state:FSMContext) -> None:
    async with state.proxy() as data:
        data["del_time"] = msg.text
    await msg.answer(text="Well. Now write please order")
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.order)
async def load_order(msg:types.Message, state:FSMContext) -> None:
    async with state.proxy() as data:
        data["order"] = msg.text
    await msg.answer(text="You'r goind good) Now write please order price")
    await OrderStatesGroup.next()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.price)
async def load_order(msg:types.Message, state:FSMContext) -> None:
    if msg.text.isdigit():
        async with state.proxy() as data:
            data["price"] = msg.text
        await msg.answer(text="Excellent 👍\nYou create a new order.")
        await sleep(1)
        await bot.send_message(chat_id=msg.from_user.id, 
                            text=f"Our order is\nAddress: {data['address']}\nPhone nomber: {data['phone']}\nDelivery time: {data['del_time']}\nOrder: {data['order']}\nPrice: {data['price']}\nEverithing is right?", reply_markup=check_keyboard)
        await OrderStatesGroup.next()
    else:
        await msg.answer(text="Please enter right price!!!")
        await OrderStatesGroup.price.set()



#________________________Order Chack block______________________

@dp.callback_query_handler(text="yes",state=OrderStatesGroup.chack)
async def right_cmd(callback:types.CallbackQuery, state:FSMContext) -> None:
    global order
    async with state.proxy() as data:
        order = data
    await callback.answer(text="Very Good!")
    mess = f"From {callback.from_user.first_name} New order\nAt {datetime.now().strftime('%d-%m %H:%M')}\n\nAddress: {order['address']}\nPhone nomber: {order['phone']}\nDelivery time: {order['del_time']}\nOrder: {order['order']}\nPrice: {order['price']}"
    await bot.send_message(chat_id=group_id, text=mess, reply_markup=courier_inl_kb)
    await callback.message.answer(text="Your order saved", reply_markup=order_button)
    await callback.message.delete()
    await state.finish()


@dp.callback_query_handler(text = "no", state=OrderStatesGroup.chack)
async def wrong_cmd(callback:types.CallbackQuery, state:FSMContext) ->None:
    global order
    async with state.proxy() as data:
        order = data
    await callback.answer(text="Houston we have problem")
    await callback.message.edit_text(text=f"Your order is\nAddress: {order['address']}\nPhone nomber: {order['phone']}\nDelivery time: {order['del_time']}\nOrder: {order['order']}\nPrice: {order['price']}\n\nWhat you want to change", reply_markup=change_keyboard)
    await OrderStatesGroup.next()


#_________________________Changes block_______________________________________

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("ch"), state=OrderStatesGroup.problem)
async def problem_command(callback:types.CallbackQuery, state:FSMContext):
    if callback.data == "ch_address":
        await callback.answer(text="Ok. Now we will change the address")
        await callback.message.answer(text="Enter right address")
        await OrderStatesGroup.change_address.set()
        await callback.message.delete()
    elif callback.data == "ch_phone":
        await callback.answer(text="Ok. Now we will change phone number")
        await callback.message.answer(text="Enter right phone number")
        await OrderStatesGroup.change_phone.set()
        await callback.message.delete()
    elif callback.data == "ch_del_time":
        await callback.answer(text="Ok. Now we will change delivery time")
        await callback.message.answer(text="Enter right time for delivery")
        await OrderStatesGroup.change_del_time.set()
        await callback.message.delete()
    elif callback.data == "ch_order":
        await callback.answer(text="Ok. Now we will change order")
        await callback.message.answer(text="Enter right order")
        await OrderStatesGroup.change_order.set()
        await callback.message.delete()
    elif callback.data == "ch_price":
        await callback.answer(text="Ok. Now we will change price")
        await callback.message.answer(text="Enter right price")
        await OrderStatesGroup.change_price.set()
        await callback.message.delete()

@dp.message_handler(content_types=["text"], state=OrderStatesGroup.change_address)
async def change_address(msg:types.Message, state = FSMContext) -> None:
    async with state.proxy() as data:
        data["address"] = msg.text
    await msg.answer(text="Ok. I change it")
    await bot.send_message(chat_id=msg.from_user.id, text=f"Your order is\nAddress: {data['address']}\nPhone nomber: {data['phone']}\nDelivery time: {data['del_time']}\nOrder: {data['order']}\nPrice: {data['price']}\n\nEverithing is right?", reply_markup=check_keyboard)
    await OrderStatesGroup.chack.set()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.change_phone)
async def change_phone(msg:types.Message, state = FSMContext) -> None:
    async with state.proxy() as data:
        data["phone"] = msg.text
    await msg.answer(text="Ok. I change it")
    await bot.send_message(chat_id=msg.from_user.id, text=f"Your order is\nAddress: {data['address']}\nPhone nomber: {data['phone']}\nDelivery time: {data['del_time']}\nOrder: {data['order']}\nPrice: {data['price']}\n\nEverithing is right?", reply_markup=check_keyboard)
    await OrderStatesGroup.chack.set()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.change_del_time)
async def change_phone(msg:types.Message, state = FSMContext) -> None:
    async with state.proxy() as data:
        data["del_time"] = msg.text
    await msg.answer(text="Ok. I change it")
    await bot.send_message(chat_id=msg.from_user.id, text=f"Your order is\nAddress: {data['address']}\nPhone nomber: {data['phone']}\nDelivery time: {data['del_time']}\nOrder: {data['order']}\nPrice: {data['price']}\n\nEverithing is right?", reply_markup=check_keyboard)
    await OrderStatesGroup.chack.set()


@dp.message_handler(content_types=["text"], state=OrderStatesGroup.change_order)
async def change_phone(msg:types.Message, state = FSMContext) -> None:
    async with state.proxy() as data:
        data["order"] = msg.text
    await msg.answer(text="Ok. I change it")
    await bot.send_message(chat_id=msg.from_user.id, text=f"Your order is\nAddress: {data['address']}\nPhone nomber: {data['phone']}\nDelivery time: {data['del_time']}\nOrder: {data['order']}\nPrice: {data['price']}\n\nEverithing is right?", reply_markup=check_keyboard)
    await OrderStatesGroup.chack.set()

@dp.message_handler(content_types=["text"], state=OrderStatesGroup.change_price)
async def change_phone(msg:types.Message, state = FSMContext) -> None:
    async with state.proxy() as data:
        data["price"] = msg.text
    await msg.answer(text="Ok. I change it")
    await bot.send_message(chat_id=msg.from_user.id, text=f"Your order is\nAddress: {data['address']}\nPhone nomber: {data['phone']}\nDelivery time: {data['del_time']}\nOrder: {data['order']}\nPrice: {data['price']}\n\nEverithing is right?", reply_markup=check_keyboard)
    await OrderStatesGroup.chack.set()


#_________________________Group admin block_______________________

@ dp.callback_query_handler(text = "courier")
async def courier_cmd(callback:types.CallbackQuery):
    await callback.answer(text="Order flyyyy))")
    await callback.message.edit_text(text=f"{callback.message.text}\n\nGiven to courier at {datetime.now().strftime('%d-%m %H:%M')}", reply_markup=costemer_inl_kb)


@ dp.callback_query_handler(text = "ord_cancel")
async def courier_cmd(callback:types.CallbackQuery):
    await callback.answer(text="BEACH")
    await callback.message.edit_text(text=f"Order Canceled\nAt {datetime.now().strftime('%d-%m %H:%M')}")


@ dp.callback_query_handler(text = "delivered")
async def courier_cmd(callback:types.CallbackQuery):
    global kassa
    global delivery_count
    await callback.answer(text="Bon Appetit")
    await callback.message.edit_text(text=f"{callback.message.text}\n\nConstemer begin to eat at {datetime.now().strftime('%d-%m %H:%M')}")
    try:
        kassa+=int((callback.message.text[callback.message.text.find("Price: ")+7:callback.message.text.find("Given")-2]))
        delivery_count+=1
        print(kassa)
        print(int((callback.message.text[(callback.message.text.find("Price: ")+7):callback.message.text.find("Given")-2])))
        print(delivery_count)   
    except:
        pass


#___________________________End and start day, Finance block_________________
#  
@dp.message_handler(commands=["End_day"])
async def cmd_order(msg:types.Message) -> None:
    global delivery_count
    global kassa
    await msg.answer(text=f"{datetime.now().strftime('%d-%m')}\n\nDelivery count: {delivery_count}\n\nKassa: {kassa}", reply_markup=new_day)


@dp.message_handler(commands=["New_day"])
async def new_day_cmd(msg:types.Message) ->None:
    global kassa
    global delivery_count
    kassa = 0
    delivery_count = 0
    await msg.answer(text=f"Good Morning {msg.from_user.first_name}",reply_markup=order_button)
    


@dp.message_handler()
async def get_msg(msg:types.Message) -> None:
    print(msg)
    await msg.reply(text=f"Sorry {msg.from_user.first_name} I can't understand you, please tipe right command")


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)