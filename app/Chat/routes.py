from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import models, schemas
from app.Chat.embeddings import get_embedding
# from langchain_community.vectorstores import PGVector
from app.authenticate.jwt import decode_token
from app.database import get_db
from app.Chat.tools import get_weather
import os
 
router = APIRouter(prefix="/chat")

@router.post("/", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest, Authorization: str = Header(...), db: Session = Depends(get_db)):
    # Decode JWT token
    token = Authorization.split(" ")[-1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token")

    # Create session
    user_id = int(payload["sub"])
    session = models.Session(user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)

    # Retrieve similar documents
    embedding = get_embedding(request.message)

    # Initialize Gemini LLM (Gemini Pro)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    if request.topic.lower() == "weather":
        prompt = f'Extract the city name from this message: "{request.message}". Only return the city name without any explanation.'
        response = llm([HumanMessage(content=prompt)])
        city = response.content.strip()
        if not city:
            answer = "Sorry, I couldn't find the city in your message."
        else:
            answer = get_weather(city)
    else:

        # Generate answer using context
        messages = [HumanMessage(content=f"Answer the following Question in detail: \n{request.message}")]
        answer = llm(messages).content

        # Store conversation
        db.add(models.Chat(session_id=session.id, role="user", content=request.message, embedding=embedding))
        db.add(models.Chat(session_id=session.id, role="assistant", content=answer))
        db.commit()

    return {"response": answer}
