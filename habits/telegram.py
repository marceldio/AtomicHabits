import os

import requests

"""Загружаем токен Telegram-бота из переменных окружения"""
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def get_chat_id_from_tg_name(tg_name):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"
    params = {"username": tg_name}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        """Возвращаем chat_id"""
        return data["result"]["id"]
    else:
        print(f"Ошибка получения chat_id: {response.text}")
        return None


def send_telegram_message(user, message):
    """Используем chat_id вместо tg_name"""
    if user.chat_id:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            """Используем сохраненный chat_id""" "chat_id": user.chat_id,
            "text": message,
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Ошибка при отправке сообщения в Telegram: {response.text}")
        else:
            print(f"Сообщение успешно отправлено для пользователя {user.email}")
