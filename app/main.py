from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import os

pipeline = None

DEFAULT_THRESHOLD = 0.85
MODEL_PATH = os.getenv('MODEL_PATH', 'models/spam_model.pkl')

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f'Файл модели не найден по пути {MODEL_PATH}')
    
    pipeline = joblib.load(MODEL_PATH)
    print(f'Модель загружена из {MODEL_PATH}')
    yield
    
    pipeline = None

app = FastAPI(
    title='Spam Detection Service',
    description='Микросервис детекции спама на базе TF-IDF + Log Regression',
    version='1.0.0',
    lifespan=lifespan
)

class MessageRequest(BaseModel):
    text: str = Field(..., description='Текст сообщения для анализа')
    threshold: float = Field(
        default=DEFAULT_THRESHOLD,
        ge=0.0,
        le=1.0,
        description='Порог отсечения спама'
    )

class PredictionResponse(BaseModel):
    is_spam: bool
    spam_probability: float
    threshold_used: float
    verdict: str
    
@app.get('/health')
def health_check():
    return {'status': 'ok', 'model_loaded': pipeline is not None}

@app.post('/predict', response_model=PredictionResponse)
def predict(request: MessageRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail='Модель не инициализирована')
    
    clean_text = request.text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail='Текст сообщения не может быть пустым')
    
    probabilities = pipeline.predict_proba([clean_text])[0]
    spam_prob = float(probabilities[1])

    is_spam = spam_prob >= request.threshold

    return PredictionResponse(
        is_spam=is_spam,
        spam_probability=round(spam_prob, 4),
        threshold_used=request.threshold,
        verdict="SPAM" if is_spam else "HAM"
    )
        