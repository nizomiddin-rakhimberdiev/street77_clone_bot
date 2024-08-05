from loader import db, dp, bot
from aiogram import types
from keyboards.default.default_keyboards import zakaz_turi
from states.all_states import YetkazishState
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_keyboards import get_categories_btn, get_products_btn, get_basket_keyboard


user_data = {}

@dp.message_handler(text="🍽 Menyu")
async def menu_handler(message: types.Message):
    await message.answer("birini tanglang", reply_markup=zakaz_turi)

@dp.message_handler(lambda message: message.text == "🛍 Savat", state='*')
async def get_basket(message: types.Message):
    user_id = message.from_user.id
    basket = db.get_my_basket(user_id)
    total_price = 0
    text = f""
    for b in basket:
        text += f"{b[1]} {b[0]}\n"
        total_price += b[2]

    text += f"Mahsulotlar: {total_price} so'm\n"
    text += "Yetkazib berish: 12 000 so'm\n"
    text += f"Jami: {total_price + 12000}"

    await message.answer(text)
  
@dp.message_handler(text="🚘 Yetkazib berish")
async def get_order(message: types.Message):
    await message.answer("Lakatsiyani yuboring")
    await YetkazishState.lokatsiya.set()

@dp.message_handler(content_types=["location"], state=YetkazishState.lokatsiya)
async def set_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await state.update_data(latitude=latitude, longitude=longitude)
    await message.answer("Kategoriyani tanlang", reply_markup= await get_categories_btn())
    await YetkazishState.category.set()

@dp.callback_query_handler(lambda c: c.data.startswith("category_"), state=YetkazishState.category)
async def get_products_handler(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data.split("_")[1]
    print(category_id)
    await call.message.answer("Productlardan birini tanlang", reply_markup=await get_products_btn(category_id))
    await YetkazishState.product.set()


@dp.callback_query_handler(lambda c: c.data.startswith("product_"), state=YetkazishState.product)
async def get_products_handler(call: types.CallbackQuery, state: FSMContext):
    product_id = int(call.data.split('_')[1])
    product = db.get_product(product_id)
    print(product)
    image = product[4]
    caption = f'{product[3]}\n{product[2]}'

    count = user_data.get(call.from_user.id, {}).get(product_id, 1)

    keyboard = await get_basket_keyboard(product_id, count)

    await call.message.answer_photo(photo=image, caption=caption, reply_markup=keyboard)
    # await state.finish()
    

@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('increment', 'decrement', 'add_to_cart')), state='*')
async def process_callback(callback_query: types.CallbackQuery):
    action, product_id = callback_query.data.split(':')
    user_id = callback_query.from_user.id
    print(user_id, 'knopkani bosdi')
    if user_id not in user_data:
        user_data[user_id] = {}
    if product_id not in user_data[user_id]:
        user_data[user_id][product_id] = 1
    
    if action == 'increment':
        user_data[user_id][product_id] += 1
    elif action == 'decrement' and user_data[user_id][product_id] > 1:
        user_data[user_id][product_id] -= 1
    elif action == 'add_to_cart':
        product_name = db.get_product_name(product_id)
        price = db.get_product_price(product_id)
        count = user_data[user_id][product_id]
        total_price = int(price) * count
        db.add_basket(user_id, product_name, count, total_price)
        await bot.send_message(
            callback_query.from_user.id,
            f"{product_name} ({count} x {price} so'm) savatchaga qo'shildi. Jami: {total_price} so'm"
        )
        return
    
    count = user_data[user_id][product_id]
    keyboard = await get_basket_keyboard(product_id, count)
    await bot.edit_message_reply_markup(
        callback_query.message.chat.id, 
        callback_query.message.message_id, 
        reply_markup=keyboard
    )
    await bot.answer_callback_query(callback_query.id)




      
 

