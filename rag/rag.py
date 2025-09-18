# import os
# import time
# import logging
# import dotenv


# dotenv.load_dotenv()

# REQUIRED_VARS = {
#     "S3_ENDPOINT": os.getenv('S3_ENDPOINT'),
#     "S3_ACCESS_KEY": os.getenv('S3_ACCESS_KEY'),
#     "S3_SECRET_KEY": os.getenv('S3_SECRET_KEY'),
#     "S3_BUCKET": os.getenv('S3_BUCKET'),
# }

# def validate_environment_variables():
#     """Проверка наличия обязательных переменных окружения"""
#     for var_name, value in REQUIRED_VARS.items():
#         if not value or value.strip().lower() == "none":
#             raise ValueError(f"{var_name} не задан. Проверьте .env.")


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# class RAG:
#     def __init__(self):


# Создаем экземпляр РАГа
# rag = RAG()

# 1.3 Проверка подключения - валидация переменных окружения
# validate_environment_variables()
# logger.info("Environment variables validation successful")
