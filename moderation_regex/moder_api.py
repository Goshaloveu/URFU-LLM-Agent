# moder_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# импортируем ваши функции из moder.py
from moder import detect_injection, get_detected_pattern

app = FastAPI(title="Moderation Patterns API", version="1.0")


class TextIn(BaseModel):
    text: str


class DetectOut(BaseModel):
    injection: bool
    detected_pattern: str = ""


@app.get("/")
def root():
    return {
        "message": 'Moderation patterns API. POST /detect with JSON {"text": "..."}'
    }


@app.post("/detect", response_model=DetectOut)
def detect(payload: TextIn):
    try:
        text = payload.text
        inj = detect_injection(text)
        pattern = get_detected_pattern(text) if inj else ""
        return DetectOut(injection=inj, detected_pattern=pattern)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Удобная команда запуска (или используйте uvicorn из CLI)
if __name__ == "__main__":
    uvicorn.run("moder_api:app", host="0.0.0.0", port=8000, reload=True)
