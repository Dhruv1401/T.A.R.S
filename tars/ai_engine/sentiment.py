from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    p = TextBlob(text).sentiment.polarity
    return "positive" if p>0.1 else "negative" if p<-0.1 else "neutral"
