from aiogram import Bot, executor, Dispatcher
from aiogram.types import Message, ContentTypes, ReplyKeyboardMarkup, KeyboardButton
from settings import API_KEY
from database import DataBase

bot = Bot(token=API_KEY)
dp = Dispatcher(bot)
database = DataBase()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(" Hello, I'm AnonymousChatBot!")

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Find a partner')
    markup.add(btn)

    await message.answer(' Press the button to find a partner', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def bot_message(message: Message):
    if message.chat.type == 'private':
        if message.text == 'Find a partner':
            partner = database.get_queue()

            if database.create_chat(message.from_user.id, partner) is False:
                database.add_queue(message.from_user.id)

                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn = KeyboardButton('Stop searching')
                markup.add(btn)

                await message.answer('Find a partner...', reply_markup=markup)

            else:
                database.delete_queue(message.from_user.id)
                database.delete_queue(partner)

                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn = KeyboardButton('Disconnect')
                markup.add(btn)

                await message.answer('You are connected to the chat!', reply_markup=markup)
                await bot.send_message(partner, 'You are connected to the chat!', reply_markup=markup)
        elif message.text == 'Disconnect':
            chat = database.get_chats(message.from_user.id)

            if chat:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn = KeyboardButton('Find a partner')
                markup.add(btn)

                await message.answer('You are disconnect from the chat!', reply_markup=markup)
                await bot.send_message(chat[1], 'Partner disconnected!', reply_markup=markup)
                database.delete_chat(message.from_user.id)
            else:
                await message.answer('You are not connected to the chat!')
        elif message.text == 'Stop searching':
            database.delete_queue(message.from_user.id)

            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn = KeyboardButton('Find a partner')
            markup.add(btn)

            await message.answer('Search stopped!', reply_markup=markup)
        else:
            chat = database.get_chats(message.chat.id)
            await bot.send_message(chat[1], message.text)
    else:
        await message.answer('Bot work only in private chat!')


@dp.message_handler(content_types=ContentTypes.VOICE)
async def voice_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_voice(chat[1], message.voice.file_id)


@dp.message_handler(content_types=ContentTypes.PHOTO)
async def photo_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_photo(chat[1], message.photo[-1].file_id)


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def document_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_document(chat[1], message.document.file_id)


@dp.message_handler(content_types=ContentTypes.VIDEO)
async def video_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_video(chat[1], message.video.file_id)


@dp.message_handler(content_types=ContentTypes.STICKER)
async def sticker_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_sticker(chat[1], message.sticker.file_id)


@dp.message_handler(content_types=ContentTypes.AUDIO)
async def audio_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_audio(chat[1], message.audio.file_id)


@dp.message_handler(content_types=ContentTypes.VIDEO_NOTE)
async def video_note_handler(message: Message):
    chat = database.get_chats(message.chat.id)

    if chat:
        await bot.send_video_note(chat[1], message.video_note.file_id)


if __name__ == '__main__':
    executor.start_polling(dp)
