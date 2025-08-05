from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

class TextToAnalyze(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    polarity: float
    subjectivity: float
    sentiment: str


@app.post("/analyze", response_model= SentimentResponse)
def analyze_sentiment(request: TextToAnalyze):
    """
    Analyze the sentiment of a given text.
    - Polarity is a float between -1.0 (negative) and 1.0 (positive).
    - Subjectivity is a float between 0.0 (objective) and 1.0 (subjective).

    """
    #TextBlow to analyze the sentiment
    blog = TextBlob(request.text)
    polarity = blog.sentiment.polarity
    subjectivity = blog.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "text" : request.text,
        "polarity" : polarity,
        "subjectivity" : subjectivity,
        "sentiment" : sentiment
    }