import logging
import jwt
import requests
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Настройки
SERVICE_ACCOUNT_ID = "ajem91na5ta32ofpeorm"  # ID сервисного аккаунта
KEY_ID = "ajehsg075bgb12f774a5"  # ID ключа сервисного аккаунта
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDZ2AgBuappw00K
V4SMYaPpSntHVu39Lpvi6NtWITmAZuXvtCYteacjk+4ubr32zvKJAM/baB0j0aiR
QgOKSptJ2VivXAfPijeRpY9nfSWMVYyP8Dc7ogHxKcSSFZMovuvNsacMwiL6GHfw
e4IcyVnRn/jtGaKCqnPIMqmZftHoOSuJeFrxEpRfu7FURdj1PYlPJbchq+W21sql
8L0Jb/jlkWfTP4/2jBX3snDFUWQCNI2P1ATEH+xLfKgxDpyXaLAb9JppGURMOGs9
tvpTODSfJaUTCbq+8wfhGZzrZdLPAe4okrMUrfP4AgeXSJpj+09ByebXf2Af0ELc
ADZFeb5dAgMBAAECggEABBqP9d6KqYYHSxlasXeV9dnLkqPhRTbd+NKlKDjlXwDR
PFnmk30Bm0TV6oExSh0zddFYU0CnWVTkdBb6rdIz4yY2h7VYEw0hSjizKr+C7FeJ
gGMFrG+vi/PmnTifR9fnFBs5PEIQ5fpmTAXG4jTC1SyEihhb8N3wKOOjErtndqAb
0Yk2tN//KhvhzpbxqMbalNBtv7wXfM2usVWv/XhfriTwt+kl9DDde9NzozfEEnfQ
20GoemHzyfvLSCTKg10LQAXLLERGFBN1Nk+7KVmKMEF/6WAmxqHXkNly4Ii37Glf
3IxMciLkvmQU1T0NHbfkQMV9WJV9mwxJJWjCQqREgQKBgQDzz6npwZHn9kd1EfHC
lRMy7BR+drxHd2hdvDXZPjRSN+75gWeumGjhVhItpa0MrJ/KUs+XXmn7Oe80miaa
Mzieagfj8xbKjfckqFmK9FCv4gci9p3EZfp6eErYwQg/CVvEfjPCX27kRNvwIzuS
nQQouC2ZCAD5B+K6iD0gbG2gHQKBgQDkvAiVYQv/y1hCfr1VwxJQRdjJ3jIHmz7W
h3VqKmjQaN711F0puw0/BocRCkt8R67ly5col//k/6fTMYzyjZmb09i6cd07DvwB
koCFg0XBAjbunzGd3sQ9HQtVUX+S1xvf/qf8yS0oyZbFgnU4I5OduV2B2eBnt4oJ
Z1bWrAbDQQKBgEAVk2m30WwRFdM1tkAZAwTdfL2I5BA82JfawqSpbwM1ZID8fI4t
zVN9ViXdaFDuhsmdXqdAz8aTAcbnxcG+OOGaqRxHZvQywIVIItEdSqAQXyPXgrx+
uYm7WKEEi/BVu2M4cM5kWzdwygainCP7VX6GeqXArtDGO9gfu0FsfpwZAoGAWdje
ikbPns+yQJRmLNzuQafeCxWDk2dQ3JXi8ivsdgjro6aiXbUC9AHNZk0j75J8yfkZ
zDFArCQcOSIammAyuXoShNIbM4qkRL3WTBuPd8w15a+Uns2VSegxvna/5N8oLOlr
9SjU21OsLLMc9ktLPcZFS69YrYTz7NOx0atLEMECgYEAlhI/uoInzop4YsQaEhum
LsmBEqNdW+sx6hS1XjzV1TBEm9Oc1YvcmnbZvwi7vYTBqbEWdB0q2OR7atRyDsZJ
VdVD/eJXc67FoEeJoW0guHfolLkmcjG5Rs0+Jv9RinhY3r5seYkNZUWs2CrBClHC
znVFPmRiDEzOsqg45PIlJ5U=
-----END PRIVATE KEY-----"""  # Закрытый ключ сервисного аккаунта
FOLDER_ID = "b1gvb5jc9dul0ok9794d"  # ID каталога Yandex Cloud
TELEGRAM_TOKEN = "8258474880:AAEFGNp7EvZDyDUjvEP_x3jRVY9r-FbLvDY"  # Токен Telegram-бота
# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class YandexGPTBot:
    def __init__(self):
        self.iam_token = None
        self.token_expires = 0

    def get_iam_token(self):
        """Получение IAM-токена (с кэшированием на 1 час)"""
        if self.iam_token and time.time() < self.token_expires:
            return self.iam_token

        try:
            now = int(time.time())
            payload = {
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': SERVICE_ACCOUNT_ID,
                'iat': now,
                'exp': now + 360
            }

            encoded_token = jwt.encode(
                payload,
                PRIVATE_KEY,
                algorithm='PS256',
                headers={'kid': KEY_ID}
            )

            response = requests.post(
                'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                json={'jwt': encoded_token},
                timeout=10
            )

            if response.status_code != 200:
                raise Exception(f"Ошибка генерации токена: {response.text}")

            token_data = response.json()
            self.iam_token = token_data['iamToken']
            self.token_expires = now + 3500  # На 100 секунд меньше срока действия

            logger.info("IAM token generated successfully")
            return self.iam_token

        except Exception as e:
            logger.error(f"Error generating IAM token: {str(e)}")
            raise

    def ask_gpt(self, question):
        """Запрос к Yandex GPT API"""
        try:
            iam_token = self.get_iam_token()

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {iam_token}',
                'x-folder-id': FOLDER_ID
            }

            data = {
                "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": 2000
                },
                "messages": [
                    {
                        "role": "user",
                        "text": question
                    }
                ]
            }

            response = requests.post(
                'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"Yandex GPT API error: {response.text}")
                raise Exception(f"Ошибка API: {response.status_code}")

            return response.json()['result']['alternatives'][0]['message']['text']

        except Exception as e:
            logger.error(f"Error in ask_gpt: {str(e)}")
            raise


# Создаем экземпляр бота
yandex_bot = YandexGPTBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Привет! Я бот для работы с Yandex GPT. Просто напиши мне свой вопрос"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    user_message = update.message.text

    if not user_message.strip():
        await update.message.reply_text("Пожалуйста, введите вопрос")
        return

    try:
        # Показываем статус "печатает"
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )

        response = yandex_bot.ask_gpt(user_message)
        await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await update.message.reply_text(
            "Извините, произошла ошибка при обработке вашего запроса. "
            "Пожалуйста, попробуйте позже."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте позже."
        )


def main():
    """Основная функция"""
    try:
        # Проверяем возможность генерации токена при запуске
        yandex_bot.get_iam_token()
        logger.info("IAM token test successful")

        application = Application.builder().token(TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)

        logger.info("Бот запускается...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")


if __name__ == "__main__":
    main()