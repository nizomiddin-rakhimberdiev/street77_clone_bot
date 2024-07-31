from loader import db, dp
from aiogram import types
from keyboards.default.default_keyboards import zakaz_turi
from states.all_states import YetkazishState
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_keyboards import get_categories_btn, get_products_btn

@dp.message_handler(text="🍽 Menyu")
async def menu_handler(message: types.Message):
    await message.answer("birini tanglang", reply_markup=zakaz_turi)
  
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
    await call.message.answer_photo(photo=image, caption=caption)
    await state.finish()
    


      
 

