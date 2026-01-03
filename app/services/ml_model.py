from enum import Enum
import torch
from transformers import AutoTokenizer, DistilBertForSequenceClassification
from newspaper import Article

class ModelPrediction(Enum):
    FAKE = 0
    REAL = 1

tokenizer = AutoTokenizer.from_pretrained("model")
model = DistilBertForSequenceClassification.from_pretrained("model", use_safetensors=True)

def get_newsletter_text(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def predict(text: str) -> tuple[ModelPrediction, float]:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    # 1. Apply softmax to convert logits to probabilities
    probs = torch.softmax(logits, dim=-1)

    # 2. Get the highest probability as the confidence score
    confidence = probs.max().item()

    # 3. Get the predicted class
    predicted_class_id = logits.argmax().item()
    prediction = ModelPrediction(predicted_class_id)

    return prediction, confidence