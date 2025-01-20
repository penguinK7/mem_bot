import logging
import os
import requests
from dotenv import load_dotenv
from telebot import TeleBot

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота
secret_token = os.getenv('TOKEN')
humor_api_key = os.getenv('HUMOR_API_KEY')
bot = TeleBot(token=secret_token)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

HUMOR_URL = 'https://humorapi.com/meme'

def get_random_meme():
    """Получение случайного мема из HumorAPI."""
    try:
        response = requests.get(HUMOR_URL, headers={'Authorization': f'Bearer {humor_api_key}'})
        response.raise_for_status()  # Проверка на успешность запроса
        data = response.json()
        return data.get('image'), data.get('caption') 
    except requests.RequestException as error:
        logging.error(f'Ошибка при запросе к API: {error}')
        return None, None

@bot.message_handler(commands=['start'])
def wake_up(message):
    """Приветственное сообщение при запуске бота."""
    chat_id = message.chat.id
    name = message.from_user.first_name

    bot.send_message(
        chat_id=chat_id,
        text=f'Здравствуйте, {name}! Этот бот отправит вам случайный мем. Используйте команду /meme для получения мема.',
    )

@bot.message_handler(commands=['meme'])
def send_meme(message):
    """Отправка случайного мема пользователю."""
    chat_id = message.chat.id
    image_url, caption = get_random_meme()

    if image_url:
        bot.send_photo(chat_id, image_url, caption=caption)
    else:
        bot.send_message(chat_id, 'Извините, произошла ошибка при получении мема.')

def main():
    """Запуск бота."""
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()