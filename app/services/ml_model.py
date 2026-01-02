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

def predict(text: str) -> ModelPrediction:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_id = logits.argmax().item()

    return ModelPrediction(predicted_class_id)