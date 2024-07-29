from loader import dp, db
from data.config import ADMINS
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from states.all_states import AddCategoryState, AddFilialState, AddProductState, GetProductState
from keyboards.default.default_keyboards import admin_menu, get_filials_btn
from keyboards.inline.inline_keyboards import get_categories_btn, get_products_btn
from geopy.geocoders import Nominatim


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in ADMINS



@dp.message_handler(AdminFilter(), commands=['start'])
async def start_admin(message: types.Message):
    await message.answer("Admin menu", reply_markup=admin_menu)




@dp.message_handler(AdminFilter(), text='Add category')
async def add_category(message: types.Message):
    await message.answer('Kategoriya nomini kiriting: ')
    await AddCategoryState.name.set()


@dp.message_handler(state=AddCategoryState.name)
async def add_category(message: types.Message, state: FSMContext):
    try:
        name = message.text
        await state.update_data(name=name)
        data = await state.get_data()
        category_name = data['name']
        db.add_category(category_name)
        await message.answer(f"Categories jadvaliga {category_name} qo'shildi")
        await state.finish()
    except Exception as e:
        await message.answer(f"Bu kategoriya mavjud, boshqa nom kiriting")
        


@dp.message_handler(text="Get category")
async def get_categories(message: types.Message):
    await message.answer("Kategoriyalar:", reply_markup=await get_categories_btn())

    

@dp.message_handler(text="Add filial")
async def add_filial(message: types.Message):
    await message.answer("Filial nomini kiriting: ")
    await AddFilialState.name.set()


@dp.message_handler(state=AddFilialState.name)
async def add_filial(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Filial locatsiyasini yuboring: ")
    await AddFilialState.lat_long.set()



@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=AddFilialState.lat_long)
async def add_filial(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    address = await get_address_from_coordinates(latitude, longitude)
    data = await state.get_data()
    name = data['name']
    db.add_filial(name, address, latitude, longitude)
    await message.answer(f"{address} fiallar jadvaliga qo'shildi")
    await state.finish()


@dp.message_handler(text="Get filial")
async def filial_handler(message: types.Message):
    await message.answer("Filiallar:", reply_markup=await get_filials_btn())

async def get_address_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="myTelegramBot/1.0")
    location = geolocator.reverse((latitude, longitude), timeout=10)
    if location:
        address = location.raw.get('address', {})
        street = address.get('road', '')
        city = address.get('city', address.get('town', address.get('village', '')))
        state = address.get('state', '')
        country = address.get('country', '')
        formatted_address = f"{street}, {city}, {state}, {country}"
        return formatted_address
    else:
        return None
    

@dp.message_handler(text='Add product')
async def add_product(message: types.Message):
    await message.answer('Maxsulot nomini kiriting: ')
    await AddProductState.name.set()


@dp.message_handler(state=AddProductState.name)
async def add_product(message: types.Message, state: FSMContext):
        name = message.text
        status = db.check_product(name)
        print(status)
        if status == None:     
            await state.update_data(name=name)
            await message.answer('Maxsulot narxi kiriting: ')
            await AddProductState.price.set()
        else:
            await message.answer(f"Bu maxsulot maxsulotlar jadvalida mavjud\nIltimos boshqa nom kiriting")

        

@dp.message_handler(state=AddProductState.price)
async def add_product(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await message.answer('Maxsulot tavsifini kiriting: ')
        await AddProductState.description.set()
    except Exception as e:
        print(e)
        await message.answer('Iltimos maxsulot narxini son bilan kiriting!')


@dp.message_handler(state=AddProductState.description)
async def add_product(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer('Maxsulot rasmini kiriting: ')
    await AddProductState.image.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AddProductState.image)
async def add_product(message: types.Message, state: FSMContext):
    image = message.photo[0].file_id
    await state.update_data(image=image)
    await message.answer('Maxsulot kategoriyasi nomini kiriting: ', reply_markup=await get_categories_btn())
    await AddProductState.category_id.set()


@dp.callback_query_handler(lambda c: c.data.startswith('category_'), state=AddProductState.category_id)
async def add_product(call: types.CallbackQuery, state: FSMContext):
    category_id = int(call.data.split('_')[1])
    await state.update_data(category_id=category_id)
    data = await state.get_data()
    name = data['name']
    price = data['price']
    description = data['description']
    image = data['image']
    category_id = data['category_id']
    db.add_product(name, price, description, image, category_id)
    await call.answer("Maxsulot qo'shildi", show_alert=True)
    await state.finish()



@dp.message_handler(text='Get product')
async def get_products(message: types.Message):
    await message.answer('Categoriyalardan birini tanlang', reply_markup=await get_categories_btn())
    await GetProductState.category.set()



@dp.callback_query_handler(lambda c: c.data.startswith('category_'), state=GetProductState.category)
async def get_products(call: types.CallbackQuery, state: FSMContext):
    category_id = int(call.data.split('_')[1])
    await call.message.answer('Productlardan birini tanlang', reply_markup=await get_products_btn(category_id))
    await GetProductState.product.set()


@dp.callback_query_handler(lambda c: c.data.startswith('product_'), state=GetProductState.product)
async def get_products(call: types.CallbackQuery, state: FSMContext):
    product_id = int(call.data.split('_')[1])
    product = db.get_product(product_id)
    print(product)
    image = product[4]
    caption = f'{product[3]}\n{product[2]}'
    await call.message.answer_photo(photo=image, caption=caption)
    await state.finish()
    