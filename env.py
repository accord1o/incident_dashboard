from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные из .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
TOKEN_EXPRESS = os.getenv("TOKEN_EXPRESS")

print(DB_USER, DB_PASSWORD, TOKEN_EXPRESS)