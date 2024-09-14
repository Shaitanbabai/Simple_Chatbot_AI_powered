import telebot
from openai import OpenAI
from gtts import gTTS
from io import BytesIO
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений из переменных окружения
API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Конфигурация клиента OpenAI
client = OpenAI(api_key=API_KEY, base_url="https://api.proxyapi.ru/openai/v1")

# Конфигурация клиента Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Словарь для хранения стилей общения пользователей
user_styles = {}

def get_response(user_message, style=""):
    """
    Генерирует ответ от модели OpenAI на основе входящего сообщения и заданного стиля общения.
    """
    instruction = f"Ответьте {style}." if style else ""
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": user_message.text}
            ],
            n=1,
            stop=None,
            temperature=0.7,
        )
        # Возвращаем сформированный ответ
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Извините, возникла ошибка при обработке вашего запроса."

@bot.message_handler(commands=['start', 'style'])
def send_welcome(message):
    """
    Отправляет приветственное сообщение с выбором стиля общения при получении команды /start или /style.
    """
    welcome_text = (
        "Привет! Этот бот поддерживает разные стили общения. Выберите один из следующих вариантов:\n"
        "1. Дружелюбный\n"
        "2. Формальный\n"
        "3. Шутливый\n"
        "4. Ввести свой стиль\n"
        "Отправьте номер выбранного стиля или напишите свой стиль после выбора 4."
    )
    bot.reply_to(message, welcome_text, reply_markup=telebot.types.ForceReply())

@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.text)
def style_choice_handler(message):
    """
    Обрабатывает выбор стиля общения, сделанный пользователем.
    """
    if message.reply_to_message.text.endswith("стиль после выбора 4."):
        process_style_choice(message)

def process_style_choice(message):
    """
    Устанавливает стиль общения на основе выбора пользователя или запрашивает ввод пользовательского стиля.
    """
    style_mapping = {"1": "дружелюбный", "2": "формальный", "3": "шутливый"}
    user_style = style_mapping.get(message.text.strip(), None)

    if user_style:
        user_styles[message.from_user.id] = user_style
        reply_text = f"Отлично! Ваш стиль общения был изменен на {user_style}."
    else:
        reply_text = "Введите ваш стиль общения:"
        bot.register_next_step_handler_by_chat_id(message.chat.id, custom_style_choice)

    bot.send_message(message.chat.id, reply_text)

def custom_style_choice(message):
    """
    Устанавливает пользовательский стиль общения, введенный пользователем.
    """
    if message.text.strip():
        user_styles[message.from_user.id] = message.text.strip()
        reply_text = f"Ваш стиль общения был изменен на '{message.text.strip()}'."
    else:
        reply_text = "Извините, не удалось распознать стиль. Пожалуйста, попробуйте еще раз, отправив /style."
    bot.send_message(message.chat.id, reply_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """
    Обрабатывает все входящие сообщения, генерирует ответ и отправляет его в виде голосового сообщения.
    """
    style = user_styles.get(message.from_user.id, "")
    response_text = get_response(message, style)

    # Генерация голосового сообщения
    tts = gTTS(response_text, lang='ru')
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)

    # Отправка голосового сообщения
    bot.send_voice(chat_id=message.chat.id, voice=audio_io)

if __name__ == "__main__":
    bot.infinity_polling()
