from fastapi import FastAPI
from app.authenticate.routes import router as auth_route
from app.Chat.routes import router as chat_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(auth_route)
app.include_router(chat_router)
