# Учебное  задание
## Телегарам-бот с подключенным GPT-чатом, выьор ролей и стиля общения

Это проект чатбота, который использует Telegram Bot API и OpenAI для обработки и генерации ответов на сообщения пользователей. Бот поддерживает различные стили общения и может отправлять ответы в виде голосовых сообщений.

## Основные возможности

- Поддержка нескольких стилей общения (дружелюбный, формальный, шутливый) и возможность ввода собственного стиля.
- Интеграция с OpenAI для генерации ответов на сообщения пользователей.
- Отправка голосовых сообщений с использованием Google Text-to-Speech (gTTS).

## Установка

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Установите необходимые зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` и добавьте в него ваши токены:

   ```
   OPENAI_API_KEY=ваш_ключ_от_openai
   TELEGRAM_TOKEN=ваш_токен_от_telegram
   ```

4. Запустите бота:

   ```bash
   python main.py
   ```

## Использование

- Отправьте команду `/start` или `/style`, чтобы выбрать стиль общения.
- После выбора стиля отправьте сообщение, и бот ответит в соответствии с выбранным стилем.
- Ответ будет отправлен в виде голосового сообщения.

## Настройка

Вы можете изменить модель OpenAI, используемую для генерации ответов, изменив параметр `model` в функции `get_response`.

## Поддержка

Если у вас возникли вопросы или проблемы, пожалуйста, создайте issue в репозитории на GitHub.

## Лицензия

Этот проект лицензирован под MIT License. Подробности в файле `LICENSE`.
